import { IsNotEmpty, IsString } from 'class-validator';
import { IsCUID } from './rules/cuid-validation';
import { ApiProperty } from '@nestjs/swagger';

export class ExecutorReqDto {
  @ApiProperty({
    description: 'user id',
    example: 'clnx2bsgi000008l68gxi8q9c',
  })
  @IsString()
  @IsCUID()
  @IsNotEmpty({ message: 'id can not be empty' })
  userId: string;
}

export class ExecutorDto {
  @ApiProperty({
    description: 'executor id',
    example: 1,
  })
  executorId: number;

  @ApiProperty({
    description: 'executor address',
    example: '0x4eD2f7bA9a0F1e2B4C4eA7Bf6fF9fE8Df0eB1E4b',
  })
  executorAddress: string;

  @ApiProperty({
    description: 'executor create time',
    example: '2023-10-20T00:00:00.000Z',
  })
  createTime: Date;
}
