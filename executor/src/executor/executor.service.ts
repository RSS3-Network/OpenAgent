import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../prisma/prisma.service';
import {
  ExecutorInfoDto,
  ExecutorReqDto,
  FundManagerReqDto,
  FundManagerRespDto,
  DepositExecutorReqDto,
  DepositExecutorRespDto,
  WithdrawExecutorReqDto,
  WithdrawExecutorRespDto,
  TransferExecutorReqDto,
  TransferExecutorRespDto,
  TxStatusReqDto,
  TxStatusRespDto,
  BalanceDto,
  ExecutorDto,
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
export class ExecutorService {
  constructor(
    private config: ConfigService,
    private prisma: PrismaService,
    @Inject('PublicClient') private readonly publicClient: any,
    @Inject('ExecutorClient') private readonly executorClient: any,
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

  async getExecutors(): Promise<ResponseDto> {
    const executors = await this.prisma.executor.findMany();

    const response: ExecutorDto[] = [];

    for (const executor of executors) {
      response.push({
        executorId: executor.executorId,
        executorAddress: executor.address,
        createTime: executor.createdAt,
      });
    }

    return {
      data: {
        items: response,
      },
    };
  }

  async getExecutorsByUserId(userId: string): Promise<ResponseDto> {
    const executorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: userId,
      },
    });

    if (!executorUser) {
      return {
        data: {
          items: [],
        },
      };
    }

    const executors = await this.prisma.executor.findMany({
      where: {
        executorUser: {
          userId: userId,
        },
      },
    });

    const response: ExecutorInfoDto[] = [];

    for (const executor of executors) {
      const executorBalance = await this.getExecutorBalance(executor.address);

      response.push({
        executorId: executor.executorId,
        executorAddress: executor.address,
        createTime: executor.createdAt,
        balance: executorBalance,
      });
    }

    return {
      data: {
        items: response,
      },
    };
  }

  async getExecutorInfo(
    userId: string,
    executorId: number,
  ): Promise<ResponseDto> {
    const executorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: userId,
      },
    });

    if (!executorUser) {
      throw new BadRequestException('not a valid user');
    }

    const executor = await this.prisma.executor.findUnique({
      where: {
        executorId: Number(executorId),
      },
    });

    if (!executor) {
      throw new BadRequestException('not a valid executor');
    }

    if (executorUser.id != executor.executorUserId) {
      throw new ForbiddenException('this executor does not belong to this user');
    }

    const executorBalance = await this.getExecutorBalance(executor.address);

    const response: ExecutorInfoDto[] = [
      {
        executorId: executor.executorId,
        executorAddress: executor.address,
        balance: executorBalance,
        createTime: executor.createdAt,
      },
    ];

    return {
      data: {
        items: response,
      },
    };
  }

  async createExecutor(dto: ExecutorReqDto): Promise<ResponseDto> {
    let executorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: dto.userId,
      },
    });

    if (!executorUser) {
      executorUser = await this.prisma.executorUser.create({
        data: {
          userId: dto.userId,
        },
      });
    }

    const { request, result } = await this.publicClient.simulateContract({
      account: this.managerAccount,
      address: this.contractAddress,
      abi: managerAbi,
      functionName: 'createExecutor',
      args: [BigInt(executorUser.id)],
    });

    const hash = await this.executorClient.writeContract(request);

    const transaction = await this.publicClient.waitForTransactionReceipt({
      hash: hash,
    });

    if (transaction.status == 'success') {
      const executorId = Number(result[0]);

      const executor = await this.prisma.executor.create({
        data: {
          executorId: executorId,
          address: result[1],
          executorUser: {
            connect: {
              id: executorUser.id,
            },
          },
        },
      });

      const response: ExecutorDto[] = [
        {
          executorId: executorId,
          executorAddress: result[1],
          createTime: executor.createdAt,
        },
      ];

      return {
        data: {
          items: response,
        },
      };
    }
  }

  async fundExecutorManager(dto: FundManagerReqDto): Promise<ResponseDto> {
    const { request } = await this.publicClient.simulateContract({
      account: this.managerAccount,
      address: this.contractAddress,
      abi: managerAbi,
      functionName: 'fund',
      value: BigInt(parseEther(String(dto.amount))),
    });

    const hash = await this.executorClient.writeContract(request);

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

  async depositExecutor(dto: DepositExecutorReqDto): Promise<ResponseDto> {
    const executorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: dto.userId,
      },
    });

    if (!executorUser) {
      throw new BadRequestException('not a valid user');
    }

    const executor = await this.prisma.executor.findUnique({
      where: {
        executorId: Number(dto.executorId),
      },
    });

    if (!executor) {
      throw new BadRequestException('not a valid executor');
    }

    if (executorUser.id != executor.executorUserId) {
      throw new ForbiddenException('this executor does not belong to this user');
    }

    const { request } = await this.publicClient.simulateContract({
      account: this.managerAccount,
      address: this.contractAddress,
      abi: managerAbi,
      functionName: 'deposit',
      args: [
        BigInt(executor.executorUserId),
        BigInt(executor.executorId),
        dto.tokenAddress,
        parseEther(String(dto.amount)),
      ],
    });

    const hash = await this.executorClient.writeContract(request);

    const transaction = await this.publicClient.waitForTransactionReceipt({
      hash: hash,
    });

    if (transaction.status == 'success') {
      const response: DepositExecutorRespDto[] = [
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

  async withdrawExecutor(dto: WithdrawExecutorReqDto): Promise<ResponseDto> {
    const txStatus = await this.prisma.txStatus.findUnique({
      where: {
        txId: dto.txId,
      },
    });

    if (txStatus) {
      throw new BadRequestException('txId already exists');
    }

    const executorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: dto.userId,
      },
    });

    if (!executorUser) {
      throw new BadRequestException('not a valid user');
    }

    const executor = await this.prisma.executor.findUnique({
      where: {
        executorId: Number(dto.executorId),
      },
    });

    if (!executor) {
      throw new BadRequestException('not a valid executor');
    }

    if (executorUser.id != executor.executorUserId) {
      throw new ForbiddenException('this executor does not belong to this user');
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
            throw new BadRequestException('not a valid `to` address');
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

    let response: WithdrawExecutorRespDto[];

    try {
      const { request } = await this.publicClient.simulateContract({
        account: this.managerAccount,
        address: this.contractAddress,
        abi: managerAbi,
        functionName: 'withdraw',
        args: [
          BigInt(executor.executorUserId),
          BigInt(executor.executorId),
          toAddr,
          dto.tokenAddress,
          amount,
        ],
      });

      const hash = await this.executorClient.writeContract(request);

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
        'insufficient balance',
      );
    }

    return {
      data: {
        items: response,
      },
    };
  }

  async transferExecutor(dto: TransferExecutorReqDto): Promise<ResponseDto> {
    const txStatus = await this.prisma.txStatus.findUnique({
      where: {
        txId: dto.txId,
      },
    });

    if (txStatus) {
      throw new BadRequestException('txId already exists');
    }

    // get from executor
    const fromExecutorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: dto.fromUserId,
      },
    });

    if (!fromExecutorUser) {
      throw new BadRequestException('not a valid user');
    }

    const fromExecutor = await this.prisma.executor.findUnique({
      where: {
        executorId: Number(dto.fromExecutorId),
      },
    });

    if (!fromExecutor) {
      throw new BadRequestException('not a valid executor');
    }

    if (fromExecutorUser.id != fromExecutor.executorUserId) {
      throw new ForbiddenException('this executor does not belong to this user');
    }

    // get to executor
    const toExecutorUser = await this.prisma.executorUser.findUnique({
      where: {
        userId: dto.toUserId,
      },
    });

    if (!toExecutorUser) {
      throw new BadRequestException('not a valid user');
    }

    const toExecutor = await this.prisma.executor.findUnique({
      where: {
        executorId: Number(dto.toExecutorId),
      },
    });

    if (!toExecutor) {
      throw new BadRequestException('not a valid executor');
    }

    if (toExecutorUser.id != toExecutor.executorUserId) {
      throw new ForbiddenException('this executor does not belong to this user');
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
          BigInt(fromExecutor.executorUserId),
          BigInt(fromExecutor.executorId),
          BigInt(toExecutor.executorUserId),
          BigInt(toExecutor.executorId),
          dto.tokenAddress,
          amount,
        ],
      });

      hash = await this.executorClient.writeContract(request);
    } catch (e) {
      throw new InternalServerErrorException(
        e.shortMessage,
        'insufficient balance',
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
      throw new BadRequestException('invalid txId or tx does not exist');
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

  async getExecutorBalance(address: string): Promise<BalanceDto[]> {
    let executorBalance: BalanceDto[];

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
        executorBalance = [];
        // add ETH balance
        executorBalance.push({
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
          executorBalance.push({
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

    for (let i = 0; i < executorBalance.length; i++) {
      if (
        executorBalance[i].tokenAddress !=
        '0x0000000000000000000000000000000000000000'
      ) {
        console.log(executorBalance[i].tokenAddress);
        const options = {
          headers: {
            accept: 'application/json',
            'x-cg-pro-api-key': this.coinGeckoApiKey,
          },
        };

        const url = `${this.coinGeckoHost}/coins/ethereum/contract/${executorBalance[i].tokenAddress}`;

        await axios
          .get(url, options)
          .then((response) => {
            executorBalance[i].tokenImageUrl = response.data.image.large;
          })
          .catch((error) => {
            console.error(error);
          });
      }
    }

    return executorBalance;
  }
}
