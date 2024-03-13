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
import { ExecutorService } from './executor.service';
import {
  ExecutorReqDto,
  ExecutorDto,
  FundManagerReqDto,
  FundManagerRespDto,
  DepositExecutorReqDto,
  DepositExecutorRespDto,
  WithdrawExecutorReqDto,
  WithdrawExecutorRespDto,
  TransferExecutorReqDto,
  TransferExecutorRespDto,
  TxStatusRespDto,
  TxStatusReqDto,
  ResponseDto,
} from './dto';
import { ApiCreatedResponse, ApiOkResponse } from '@nestjs/swagger';
import { ExecutorInfoDto } from './dto';

@Controller('executors')
export class ExecutorController {
  constructor(private executorService: ExecutorService) {}

  @ApiOkResponse({
    description: 'The executors has been successfully queried.',
    type: ExecutorDto,
    isArray: true,
  })
  @Get()
  getExecutors() {
    return this.executorService.getExecutors();
  }

  @ApiOkResponse({
    description: 'The executors has been successfully queried.',
    type: ExecutorInfoDto,
    isArray: true,
  })
  @Get(':userId')
  getExecutorsByUserId(@Param('userId') userId: string) {
    return this.executorService.getExecutorsByUserId(userId);
  }

  @ApiOkResponse({
    description: 'The executor has been successfully queried.',
    type: ExecutorInfoDto,
  })
  @Get(':userId/:executorId')
  getExecutor(
    @Param('userId') userId: string,
    @Param('executorId') executorId: number,
  ): Promise<ResponseDto> {
    return this.executorService.getExecutorInfo(userId, executorId);
  }

  @ApiCreatedResponse({
    description: 'The executor has been successfully created.',
    type: ExecutorDto,
  })
  @Post()
  create(@Body() executorReqDto: ExecutorReqDto): Promise<ResponseDto> {
    return this.executorService.createExecutor(executorReqDto);
  }

  @ApiOkResponse({
    description: 'The manager contract has been successfully funded.',
    type: FundManagerRespDto,
  })
  @Post('fund')
  @HttpCode(200)
  fund(@Body() fundManagerReqDto: FundManagerReqDto): Promise<ResponseDto> {
    return this.executorService.fundExecutorManager(fundManagerReqDto);
  }

  @ApiOkResponse({
    description: 'The executor has been successfully deposit.',
    type: DepositExecutorRespDto,
  })
  @Post('deposit')
  @HttpCode(200)
  deposit(
    @Body() depositExecutorReqDto: DepositExecutorReqDto,
  ): Promise<ResponseDto> {
    return this.executorService.depositExecutor(depositExecutorReqDto);
  }

  @ApiOkResponse({
    description: 'The token has been successfully withdraw.',
    type: WithdrawExecutorRespDto,
  })
  @Post('withdraw')
  @HttpCode(200)
  withdraw(
    @Body() withdrawExecutorReqDto: WithdrawExecutorReqDto,
  ): Promise<ResponseDto> {
    return this.executorService.withdrawExecutor(withdrawExecutorReqDto);
  }

  @ApiOkResponse({
    description: 'The token has been successfully transfered.',
    type: TransferExecutorRespDto,
  })
  @Post('transfer')
  @HttpCode(200)
  transfer(
    @Body() transferExecutorReqDto: TransferExecutorReqDto,
  ): Promise<ResponseDto> {
    return this.executorService.transferExecutor(transferExecutorReqDto);
  }

  @ApiOkResponse({
    description: 'Query tx status by txId',
    type: TxStatusRespDto,
  })
  @Post('tx/status')
  @HttpCode(200)
  getTxStatus(@Body() txStatusReqDto: TxStatusReqDto): Promise<ResponseDto> {
    return this.executorService.getTxStatus(txStatusReqDto);
  }
}
