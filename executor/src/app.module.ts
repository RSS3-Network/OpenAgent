import { Module } from '@nestjs/common';
import { ExecutorController } from './executor/executor.controller';
import { ExecutorService } from './executor/executor.service';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module';
import { createPublicClient, http, createWalletClient, Hex } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { sepolia } from 'viem/chains';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    PrismaModule,
  ],
  controllers: [ExecutorController],
  providers: [
    ExecutorService,
    {
      provide: 'PublicClient',
      useFactory: (configService: ConfigService) => {
        const publicClient = createPublicClient({
          chain: sepolia,
          transport: http(configService.get('EXECUTOR_RPC_URL')),
        });

        return publicClient;
      },
      inject: [ConfigService],
    },
    {
      provide: 'ExecutorClient',
      useFactory: (configService: ConfigService) => {
        // Local Account
        const account = privateKeyToAccount(
          configService.get<Hex>('EXECUTOR_PRIVATE_KEY'),
        );

        const executorClient = createWalletClient({
          account,
          chain: sepolia,
          transport: http(configService.get('EXECUTOR_RPC_URL')),
        });

        return executorClient;
      },
      inject: [ConfigService],
    },
    {
      provide: 'ManagerAccount',
      useFactory: (configService: ConfigService) => {
        // Local Account
        const account = privateKeyToAccount(
          configService.get<Hex>('EXECUTOR_PRIVATE_KEY'),
        );

        return account;
      },
      inject: [ConfigService],
    },
    {
      provide: 'ContractAddress',
      useFactory: (configService: ConfigService) => {
        // Local Account
        const account = configService.get(
          'EXECUTOR_CONTRACT_ADDRESS',
        );

        return account;
      },
      inject: [ConfigService],
    },
    {
      provide: 'EthereumExplorerUrl',
      useFactory: (configService: ConfigService) => {
        const url = configService.get('ETHEREUM_EXPLORER_URL');

        return url;
      },
      inject: [ConfigService],
    },
    {
      provide: 'EthereumExplorerApiKey',
      useFactory: (configService: ConfigService) => {
        const key = configService.get('ETHEREUM_EXPLORER_API_KEY');

        return key;
      },
      inject: [ConfigService],
    },
    {
      provide: 'CoinGeckoHost',
      useFactory: (configService: ConfigService) => {
        const host = configService.get('COINGECKO_HOST');

        return host;
      },
      inject: [ConfigService],
    },
    {
      provide: 'CoinGeckoApiKey',
      useFactory: (configService: ConfigService) => {
        const key = configService.get('COINGECKO_API_KEY');

        return key;
      },
      inject: [ConfigService],
    },
  ],
})
export class AppModule {}
