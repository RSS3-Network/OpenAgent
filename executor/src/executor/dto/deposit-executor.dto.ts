import { IsNotEmpty, IsString, IsUUID } from 'class-validator';
import { IsCUID } from './rules/cuid-validation';
import { ApiProperty } from '@nestjs/swagger';

export class DepositExecutorReqDto {
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
}

export class DepositExecutorRespDto {
  @ApiProperty({
    description: 'hash',
    example: '0x1234567890',
  })
  hash: string;
}
