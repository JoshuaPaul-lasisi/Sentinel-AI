import { IsNotEmpty, IsNumber, IsString } from 'class-validator';

export class CreateTransactionDto {
  @IsNumber()
  @IsNotEmpty()
  amount: number;
  @IsString()
  @IsNotEmpty()
  user_id: string;
  @IsString()
  @IsNotEmpty()
  timestamp: string;
  @IsString()
  @IsNotEmpty()
  device_id: string;
  @IsString()
  @IsNotEmpty()
  location: string;
  @IsNumber()
  bvn_age_hours?: number;
}

export class TransactionDto {
    id: string;
    amount: number;
    user_id: string;
    timestamp: string;
    device_id: string;
    location: string;
    bvn_age_hours?: number;
    risk_score: number;
    status: 'APPROVED' | 'REVIEW' | 'BLOCKED';
    type: string;
  }
  

  
  export class TransactionResponseDto {
    id: string;
    amount: number;
    user_id: string;
    timestamp: string;
    device_id: string;
    location: string;
    bvn_age_hours?: number;
    risk_score: number;
    status: string;
    type: string;
    ml_explanation?: any;
  }
  
  export class StatsResponseDto {
    totalTransactions: number;
    fraudDetected: number;
    moneySaved: string;
    avgResponseTime: string;
    totalAmountProcessed: number;
  }