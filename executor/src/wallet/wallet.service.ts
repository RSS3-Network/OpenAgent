import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../prisma/prisma.service';
import {
  WalletInfoDto,
  WalletReqDto,
  FundManagerReqDto,
  FundManagerRespDto,
  DepositWalletReqDto,
  DepositWalletRespDto,
  WithdrawWalletReqDto,
  WithdrawWalletRespDto,
  TransferWalletReqDto,
  TransferWalletRespDto,
  TxStatusReqDto,
  TxStatusRespDto,
  BalanceDto,
  WalletDto,
  ResponseDto,
} from './dto';
import {
  Injectable,
  Inject,
  ForbiddenException,
  NotFoundException,
  BadRequestException,
  InternalServerErrorException,
} from '@nestjs/common';
import { managerAbi } from './contract/abi';
import { parseEther, isAddress } from 'viem';
import axios from 'axios';

@Injectable()
export class WalletService {
  constructor(
    private config: ConfigService,
    private prisma: PrismaService,
    @Inject('PublicClient') private readonly publicClient: any,
    @Inject('WalletClient') private readonly walletClient: any,
    @Inject('ManagerAccount') private readonly managerAccount: any,
    @Inject('ContractAddress') private readonly contractAddress: any,
    @Inject('EthereumExplorerUrl') private readonly ethereumExplorerUrl: any,
    @Inject('EthereumExplorerApiKey')
    private readonly ethereumExplorerApiKey: any,
    @Inject('CoinGeckoHost')
    private readonly coinGeckoHost: any,
    @Inject('CoinGeckoApiKey')
    private readonly coinGeckoApiKey: any,
  ) {}

  async getWallets(): Promise<ResponseDto> {
    const wallets = await this.prisma.wallet.findMany();

    const response: WalletDto[] = [];

    for (const wallet of wallets) {
      response.push({
        walletId: wallet.walletId,
        walletAddress: wallet.address,
        createTime: wallet.createdAt,
      });
    }

    return {
      data: {
        items: response,
      },
    };
  }

  async getWalletsByUserId(userId: string): Promise<ResponseDto> {
    const walletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: userId,
      },
    });

    if (!walletUser) {
      return {
        data: {
          items: [],
        },
      };
    }

    const wallets = await this.prisma.wallet.findMany({
      where: {
        walletUser: {
          userId: userId,
        },
      },
    });

    const response: WalletInfoDto[] = [];

    for (const wallet of wallets) {
      const walletBalance = await this.getWalletBalance(wallet.address);

      response.push({
        walletId: wallet.walletId,
        walletAddress: wallet.address,
        createTime: wallet.createdAt,
        balance: walletBalance,
      });
    }

    return {
      data: {
        items: response,
      },
    };
  }

  async getWalletInfo(userId: string, walletId: number): Promise<ResponseDto> {
    const walletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: userId,
      },
    });

    if (!walletUser) {
      throw new BadRequestException('not valid user');
    }

    const wallet = await this.prisma.wallet.findUnique({
      where: {
        walletId: Number(walletId),
      },
    });

    if (!wallet) {
      throw new BadRequestException('not valid wallet');
    }

    if (walletUser.id != wallet.walletUserId) {
      throw new ForbiddenException('this wallet is not belong to this user');
    }

    const walletBalance = await this.getWalletBalance(wallet.address);

    const response: WalletInfoDto[] = [
      {
        walletId: wallet.walletId,
        walletAddress: wallet.address,
        balance: walletBalance,
        createTime: wallet.createdAt,
      },
    ];

    return {
      data: {
        items: response,
      },
    };
  }

  async createWallet(dto: WalletReqDto): Promise<ResponseDto> {
    let walletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: dto.userId,
      },
    });

    if (!walletUser) {
      walletUser = await this.prisma.walletUser.create({
        data: {
          userId: dto.userId,
        },
      });
    }

    const { request, result } = await this.publicClient.simulateContract({
      account: this.managerAccount,
      address: this.contractAddress,
      abi: managerAbi,
      functionName: 'createWallet',
      args: [BigInt(walletUser.id)],
    });

    const hash = await this.walletClient.writeContract(request);

    const transaction = await this.publicClient.waitForTransactionReceipt({
      hash: hash,
    });

    if (transaction.status == 'success') {
      const walletId = Number(result[0]);

      const wallet = await this.prisma.wallet.create({
        data: {
          walletId: walletId,
          address: result[1],
          walletUser: {
            connect: {
              id: walletUser.id,
            },
          },
        },
      });

      const response: WalletDto[] = [
        {
          walletId: walletId,
          walletAddress: result[1],
          createTime: wallet.createdAt,
        },
      ];

      return {
        data: {
          items: response,
        },
      };
    }
  }

  async fundWalletManager(dto: FundManagerReqDto): Promise<ResponseDto> {
    const { request } = await this.publicClient.simulateContract({
      account: this.managerAccount,
      address: this.contractAddress,
      abi: managerAbi,
      functionName: 'fund',
      value: BigInt(parseEther(String(dto.amount))),
    });

    const hash = await this.walletClient.writeContract(request);

    const transaction = await this.publicClient.waitForTransactionReceipt({
      hash: hash,
    });

    if (transaction.status == 'success') {
      const response: FundManagerRespDto[] = [
        {
          hash,
        },
      ];

      return {
        data: {
          items: response,
        },
      };
    }
  }

  async depositWallet(dto: DepositWalletReqDto): Promise<ResponseDto> {
    const walletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: dto.userId,
      },
    });

    if (!walletUser) {
      throw new BadRequestException('not valid user');
    }

    const wallet = await this.prisma.wallet.findUnique({
      where: {
        walletId: Number(dto.walletId),
      },
    });

    if (!wallet) {
      throw new BadRequestException('not valid wallet');
    }

    if (walletUser.id != wallet.walletUserId) {
      throw new ForbiddenException('this wallet is not belong to this user');
    }

    const { request } = await this.publicClient.simulateContract({
      account: this.managerAccount,
      address: this.contractAddress,
      abi: managerAbi,
      functionName: 'deposit',
      args: [
        BigInt(wallet.walletUserId),
        BigInt(wallet.walletId),
        dto.tokenAddress,
        parseEther(String(dto.amount)),
      ],
    });

    const hash = await this.walletClient.writeContract(request);

    const transaction = await this.publicClient.waitForTransactionReceipt({
      hash: hash,
    });

    if (transaction.status == 'success') {
      const response: DepositWalletRespDto[] = [
        {
          hash,
        },
      ];

      return {
        data: {
          items: response,
        },
      };
    }
  }

  async withdrawWallet(dto: WithdrawWalletReqDto): Promise<ResponseDto> {
    const txStatus = await this.prisma.txStatus.findUnique({
      where: {
        txId: dto.txId,
      },
    });

    if (txStatus) {
      throw new BadRequestException('txId already exist');
    }

    const walletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: dto.userId,
      },
    });

    if (!walletUser) {
      throw new BadRequestException('not valid user');
    }

    const wallet = await this.prisma.wallet.findUnique({
      where: {
        walletId: Number(dto.walletId),
      },
    });

    if (!wallet) {
      throw new BadRequestException('not valid wallet');
    }

    if (walletUser.id != wallet.walletUserId) {
      throw new ForbiddenException('this wallet is not belong to this user');
    }

    let toAddr = dto.toAddress;

    if (!isAddress(dto.toAddress)) {
      const options = {
        headers: {
          accept: 'application/json',
        },
      };

      await axios
        .get(
          `https://testnet.rss3.io/data/accounts/${dto.toAddress}/profiles`,
          options,
        )
        .then((response) => {
          const ethereumEntries = response.data.data.filter(
            (item) => item.network === 'ethereum',
          );
          if (ethereumEntries.length > 0) {
            toAddr = ethereumEntries[0].address;
          } else {
            throw new BadRequestException('not valid to address');
          }
        })
        .catch((error) => {
          console.error(error);
        });
    }

    let amount: BigInt;
    if (dto.tokenAddress == '0x0000000000000000000000000000000000000000') {
      amount = parseEther(String(dto.amount));
    } else {
      amount = BigInt(dto.amount * 10 ** dto.tokenDecimal);
    }

    let response: WithdrawWalletRespDto[];

    try {
      const { request } = await this.publicClient.simulateContract({
        account: this.managerAccount,
        address: this.contractAddress,
        abi: managerAbi,
        functionName: 'withdraw',
        args: [
          BigInt(wallet.walletUserId),
          BigInt(wallet.walletId),
          toAddr,
          dto.tokenAddress,
          amount,
        ],
      });

      const hash = await this.walletClient.writeContract(request);

      await this.prisma.txStatus.create({
        data: {
          txId: dto.txId,
          hash: hash,
          status: 'initiated',
          payload: JSON.stringify(dto),
        },
      });

      response = [
        {
          hash: hash,
        },
      ];
    } catch (e) {
      throw new InternalServerErrorException(
        e.shortMessage,
        'not sufficient balance',
      );
    }

    return {
      data: {
        items: response,
      },
    };
  }

  async transferWallet(dto: TransferWalletReqDto): Promise<ResponseDto> {
    const txStatus = await this.prisma.txStatus.findUnique({
      where: {
        txId: dto.txId,
      },
    });

    if (txStatus) {
      throw new BadRequestException('txId already exist');
    }

    // get from wallet
    const fromWalletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: dto.fromUserId,
      },
    });

    if (!fromWalletUser) {
      throw new BadRequestException('not valid user');
    }

    const fromWallet = await this.prisma.wallet.findUnique({
      where: {
        walletId: Number(dto.fromWalletId),
      },
    });

    if (!fromWallet) {
      throw new BadRequestException('not valid wallet');
    }

    if (fromWalletUser.id != fromWallet.walletUserId) {
      throw new ForbiddenException('this wallet is not belong to this user');
    }

    // get to wallet
    const toWalletUser = await this.prisma.walletUser.findUnique({
      where: {
        userId: dto.toUserId,
      },
    });

    if (!toWalletUser) {
      throw new BadRequestException('not valid user');
    }

    const toWallet = await this.prisma.wallet.findUnique({
      where: {
        walletId: Number(dto.toWalletId),
      },
    });

    if (!toWallet) {
      throw new BadRequestException('not valid wallet');
    }

    if (toWalletUser.id != toWallet.walletUserId) {
      throw new ForbiddenException('this wallet is not belong to this user');
    }

    let amount: BigInt;
    if (dto.tokenAddress == '0x0000000000000000000000000000000000000000') {
      amount = parseEther(String(dto.amount));
    } else {
      amount = BigInt(dto.amount * 10 ** dto.tokenDecimal);
    }

    let hash: string;

    try {
      const { request } = await this.publicClient.simulateContract({
        account: this.managerAccount,
        address: this.contractAddress,
        abi: managerAbi,
        functionName: 'transfer',
        args: [
          BigInt(fromWallet.walletUserId),
          BigInt(fromWallet.walletId),
          BigInt(toWallet.walletUserId),
          BigInt(toWallet.walletId),
          dto.tokenAddress,
          amount,
        ],
      });

      hash = await this.walletClient.writeContract(request);
    } catch (e) {
      throw new InternalServerErrorException(
        e.shortMessage,
        'not sufficient balance',
      );
    }

    await this.prisma.txStatus.create({
      data: {
        txId: dto.txId,
        hash,
        status: 'initiated',
        payload: JSON.stringify(dto),
      },
    });

    const response = [
      {
        hash,
      },
    ];

    return {
      data: {
        items: response,
      },
    };
  }

  async getTxStatus(dto: TxStatusReqDto): Promise<ResponseDto> {
    let txStatus = await this.prisma.txStatus.findUnique({
      where: {
        txId: dto.txId,
      },
    });

    if (!txStatus) {
      throw new BadRequestException('invalid txId or tx not exist');
    }

    let transaction;
    try {
      transaction = await this.publicClient.getTransactionReceipt({
        hash: txStatus.hash,
      });
    } catch (e) {
      throw new InternalServerErrorException(e.shortMessage);
    }

    txStatus = await this.prisma.txStatus.update({
      where: {
        txId: dto.txId,
      },
      data: {
        status: transaction.status,
      },
    });

    const response: TxStatusRespDto[] = [
      {
        txId: dto.txId,
        status: txStatus.status,
        txHash: txStatus.hash,
        txPayload: JSON.parse(txStatus.payload),
      },
    ];

    return {
      data: {
        items: response,
      },
    };
  }

  async getWalletBalance(address: string): Promise<BalanceDto[]> {
    let walletBalance: BalanceDto[];

    // fetch balance
    const options = {
      headers: {
        accept: 'application/json',
      },
    };

    const url = `${this.ethereumExplorerUrl}/getAddressInfo/${address}?apiKey=${this.ethereumExplorerApiKey}`;

    await axios
      .get(url, options)
      .then((response) => {
        walletBalance = [];
        // add ETH balance
        walletBalance.push({
          tokenAddress: '0x0000000000000000000000000000000000000000',
          tokenName: 'ETH',
          tokenSymbol: 'ETH',
          tokenDecimal: 18,
          tokenBalance: response.data.ETH.rawBalance,
          tokenImageUrl:
            'https://assets.coingecko.com/coins/images/279/large/ethereum.png?1696501628',
        });

        // add token balances
        response.data.tokens.forEach((token: any) => {
          walletBalance.push({
            tokenAddress: token.tokenInfo.address,
            tokenName: token.tokenInfo.name,
            tokenSymbol: token.tokenInfo.symbol,
            tokenDecimal: token.tokenInfo.decimals,
            tokenBalance: token.rawBalance,
            tokenImageUrl:
              'https://assets.coingecko.com/coins/images/279/large/ethereum.png?1696501628',
          });
        });
      })
      .catch((error) => {
        console.error(error);
      });

    for (let i = 0; i < walletBalance.length; i++) {
      if (
        walletBalance[i].tokenAddress !=
        '0x0000000000000000000000000000000000000000'
      ) {
        console.log(walletBalance[i].tokenAddress);
        const options = {
          headers: {
            accept: 'application/json',
            'x-cg-pro-api-key': this.coinGeckoApiKey,
          },
        };

        const url = `${this.coinGeckoHost}/coins/ethereum/contract/${walletBalance[i].tokenAddress}`;

        await axios
          .get(url, options)
          .then((response) => {
            walletBalance[i].tokenImageUrl = response.data.image.large;
          })
          .catch((error) => {
            console.error(error);
          });
      }
    }

    return walletBalance;
  }
}
