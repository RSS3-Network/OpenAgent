import { ApiProperty } from '@nestjs/swagger';

export class ExecutorInfoDto {
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
    description: 'executor balance',
    example: '1000',
  })
  balance: BalanceDto[];

  @ApiProperty({
    description: 'executor create time',
    example: '2023-10-20T00:00:00.000Z',
  })
  createTime: Date;
}

export class BalanceDto {
  @ApiProperty({
    description: 'token address',
    example: '0x000',
  })
  tokenAddress: string;

  @ApiProperty({
    description: 'token name',
    example: 'USDT',
  })
  tokenName: string;

  @ApiProperty({
    description: 'token symbol',
    example: 'USDT',
  })
  tokenSymbol: string;

  @ApiProperty({
    description: 'token decimal',
    example: 18,
  })
  tokenDecimal: number;

  @ApiProperty({
    description: 'token balance',
    example: '1000',
  })
  tokenBalance: string;

  @ApiProperty({
    description: 'token image url',
    example: 'image url',
  })
  tokenImageUrl: string;
}
