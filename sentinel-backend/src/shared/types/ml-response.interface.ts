export interface IMLResponse {
  risk_score: number;
  explanation: {
    features: Array<{ name: string; contribution: number; value: any }>;
  };
  recommendation: 'APPROVE' | 'REVIEW' | 'BLOCK';
}
