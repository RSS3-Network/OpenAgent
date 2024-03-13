import { IsNotEmpty, IsString, IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class FundManagerReqDto {
  @ApiProperty({
    description: 'amount',
    example: 0.1,
  })
  @IsNotEmpty({ message: 'amount can not be empty' })
  amount: number;
}

export class FundManagerRespDto {
  @ApiProperty({
    description: 'hash',
    example: '0x1234567890',
  })
  hash: string;
}
