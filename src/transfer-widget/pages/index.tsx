import { useRouter } from 'next/router';
import TransferWidget from '../components/TransferWidget';

export default function Home() {
  const router = useRouter();
  const { token, amount, toAddress, chainName } = router.query;

  return (
    <TransferWidget
      token={token as string}
      amount={amount as string}
      toAddress={toAddress as string}
      chainName={chainName as string}
    />
  );
}