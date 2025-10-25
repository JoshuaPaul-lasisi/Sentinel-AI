import { Injectable } from '@nestjs/common';
import { MlService } from 'src/ml/ml.service';

@Injectable()
export class TransactionsService {
  constructor(private readonly mlService: MlService) {}
  async analyzeTransaction(transactionData: any) {
    // return transactionData;
    const prediction = await this.mlService.predict(transactionData);
    return {
      transactionData,
      risk: prediction.risk_score,
      explanation: prediction.explanation,
      recommendation: prediction.recommendation,
    };
  }
}
