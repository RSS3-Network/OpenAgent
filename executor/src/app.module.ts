import { Module } from '@nestjs/common';
import { WalletController } from './wallet/wallet.controller';
import { WalletService } from './wallet/wallet.service';
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
  controllers: [WalletController],
  providers: [
    WalletService,
    {
      provide: 'PublicClient',
      useFactory: (configService: ConfigService) => {
        const publicClient = createPublicClient({
          chain: sepolia,
          transport: http(configService.get('OPENAGENT_WALLET_RPC_URL')),
        });

        return publicClient;
      },
      inject: [ConfigService],
    },
    {
      provide: 'WalletClient',
      useFactory: (configService: ConfigService) => {
        // Local Account
        const account = privateKeyToAccount(
          configService.get<Hex>('OPENAGENT_WALLET_PRIVATE_KEY'),
        );

        const walletClient = createWalletClient({
          account,
          chain: sepolia,
          transport: http(configService.get('OPENAGENT_WALLET_RPC_URL')),
        });

        return walletClient;
      },
      inject: [ConfigService],
    },
    {
      provide: 'ManagerAccount',
      useFactory: (configService: ConfigService) => {
        // Local Account
        const account = privateKeyToAccount(
          configService.get<Hex>('OPENAGENT_WALLET_PRIVATE_KEY'),
        );

        return account;
      },
      inject: [ConfigService],
    },
    {
      provide: 'ContractAddress',
      useFactory: (configService: ConfigService) => {
        // Local Account
        const account = configService.get('OPENAGENT_WALLET_CONTRACT_ADDRESS');

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
