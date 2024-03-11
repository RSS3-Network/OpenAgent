import { IsNotEmpty, IsString, IsUUID } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export class TxStatusReqDto {
  @ApiProperty({
    description: 'tx id (in uuid format)',
    example: 'f912165a-cf8b-4c18-8596-212c49b8ebbf',
  })
  @IsString()
  @IsUUID()
  @IsNotEmpty({ message: 'tx id can not be empty' })
  txId: string;
}

export class TxStatusRespDto {
  @ApiProperty({
    description: 'tx id (in uuid format)',
    example: 'f912165a-cf8b-4c18-8596-212c49b8ebbf',
  })
  txId: string;

  @ApiProperty({
    description: 'status',
    example: 'success',
  })
  status: string;

  @ApiProperty({
    description: 'tx payload',
    example: '{}',
  })
  txPayload: string;

  @ApiProperty({
    description: 'tx hash',
    example: '0x1234567890',
  })
  txHash: string;
}
