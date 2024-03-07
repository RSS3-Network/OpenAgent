import {
  Body,
  Controller,
  HttpCode,
  HttpStatus,
  Post,
  Get,
  Query,
  Param,
  Put,
  Delete,
} from '@nestjs/common';
import { WalletService } from './wallet.service';
import {
  WalletReqDto,
  WalletDto,
  FundManagerReqDto,
  FundManagerRespDto,
  DepositWalletReqDto,
  DepositWalletRespDto,
  WithdrawWalletReqDto,
  WithdrawWalletRespDto,
  TransferWalletReqDto,
  TransferWalletRespDto,
  TxStatusRespDto,
  TxStatusReqDto,
  ResponseDto,
} from './dto';
import { ApiCreatedResponse, ApiOkResponse } from '@nestjs/swagger';
import { WalletInfoDto } from './dto';

@Controller('wallets')
export class WalletController {
  constructor(private walletService: WalletService) {}

  @ApiOkResponse({
    description: 'The wallets has been successfully queried.',
    type: WalletDto,
    isArray: true,
  })
  @Get()
  getWallets() {
    return this.walletService.getWallets();
  }

  @ApiOkResponse({
    description: 'The wallets has been successfully queried.',
    type: WalletInfoDto,
    isArray: true,
  })
  @Get(':userId')
  getWalletsByUserId(@Param('userId') userId: string) {
    return this.walletService.getWalletsByUserId(userId);
  }

  @ApiOkResponse({
    description: 'The wallet has been successfully queried.',
    type: WalletInfoDto,
  })
  @Get(':userId/:walletId')
  getWallet(
    @Param('userId') userId: string,
    @Param('walletId') walletId: number,
  ): Promise<ResponseDto> {
    return this.walletService.getWalletInfo(userId, walletId);
  }

  @ApiCreatedResponse({
    description: 'The wallet has been successfully created.',
    type: WalletDto,
  })
  @Post()
  create(@Body() walletReqDto: WalletReqDto): Promise<ResponseDto> {
    return this.walletService.createWallet(walletReqDto);
  }

  @ApiOkResponse({
    description: 'The manager contract has been successfully funded.',
    type: FundManagerRespDto,
  })
  @Post('fund')
  @HttpCode(200)
  fund(@Body() fundManagerReqDto: FundManagerReqDto): Promise<ResponseDto> {
    return this.walletService.fundWalletManager(fundManagerReqDto);
  }

  @ApiOkResponse({
    description: 'The wallet has been successfully deposit.',
    type: DepositWalletRespDto,
  })
  @Post('deposit')
  @HttpCode(200)
  deposit(
    @Body() depositWalletReqDto: DepositWalletReqDto,
  ): Promise<ResponseDto> {
    return this.walletService.depositWallet(depositWalletReqDto);
  }

  @ApiOkResponse({
    description: 'The token has been successfully withdraw.',
    type: WithdrawWalletRespDto,
  })
  @Post('withdraw')
  @HttpCode(200)
  withdraw(
    @Body() withdrawWalletReqDto: WithdrawWalletReqDto,
  ): Promise<ResponseDto> {
    return this.walletService.withdrawWallet(withdrawWalletReqDto);
  }

  @ApiOkResponse({
    description: 'The token has been successfully transfered.',
    type: TransferWalletRespDto,
  })
  @Post('transfer')
  @HttpCode(200)
  transfer(
    @Body() transferWalletReqDto: TransferWalletReqDto,
  ): Promise<ResponseDto> {
    return this.walletService.transferWallet(transferWalletReqDto);
  }

  @ApiOkResponse({
    description: 'Query tx status by txId',
    type: TxStatusRespDto,
  })
  @Post('tx/status')
  @HttpCode(200)
  getTxStatus(@Body() txStatusReqDto: TxStatusReqDto): Promise<ResponseDto> {
    return this.walletService.getTxStatus(txStatusReqDto);
  }
}
