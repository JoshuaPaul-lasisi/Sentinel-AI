import { Module } from '@nestjs/common';
import { TransactionsController } from './transactions.controller';
import { TransactionsService } from './transactions.service';
import { MlModule } from 'src/ml/ml.module';

@Module({
  controllers: [TransactionsController],
  providers: [TransactionsService], 
  imports : [MlModule],
})
export class TransactionsModule {}
