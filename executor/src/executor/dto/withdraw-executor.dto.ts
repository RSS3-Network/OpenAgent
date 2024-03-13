import { IsNotEmpty, IsString, IsUUID } from 'class-validator';
import { IsCUID } from './rules/cuid-validation';
import { ApiProperty } from '@nestjs/swagger';

export class WithdrawExecutorReqDto {
  @ApiProperty({
    description: 'tx id (in uuid format)',
    example: 'f912165a-cf8b-4c18-8596-212c49b8ebbf',
  })
  @IsString()
  @IsUUID()
  @IsNotEmpty({ message: 'tx id can not be empty' })
  txId: string;

  @ApiProperty({
    description: 'user id',
    example: 'clnx2bsgi000008l68gxi8q9c',
  })
  @IsString()
  @IsCUID()
  @IsNotEmpty({ message: 'id can not be empty' })
  userId: string;

  @ApiProperty({
    description: 'executor id',
    example: 1,
  })
  @IsNotEmpty({ message: 'executor id can not be empty' })
  executorId: number;

  @ApiProperty({
    description: 'to address',
    example: '0x00',
  })
  @IsNotEmpty({ message: 'to address can not be empty' })
  toAddress: string;

  @ApiProperty({
    description: 'amount',
    example: 0.01,
  })
  @IsNotEmpty({ message: 'amount can not be empty' })
  amount: number;

  @ApiProperty({
    description: 'token address',
    example: '0x0000000000000000000000000000000000000000',
  })
  @IsNotEmpty({ message: 'token address can not be empty' })
  tokenAddress: string;

  @ApiProperty({
    description: 'decimal',
    example: 6,
  })
  @IsNotEmpty({ message: 'decimal can not be empty' })
  tokenDecimal: number;
}

export class WithdrawExecutorRespDto {
  @ApiProperty({
    description: 'hash',
    example: '0x1234567890',
  })
  hash: string;
}
