export interface Transaction {
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
  
  export interface MLResponse {
    risk_score: number;
    explanation: {
      features: Array<{
        name: string;
        contribution: number;
        value: unknown;
      }>;
    };
    recommendation: 'APPROVE' | 'REVIEW' | 'BLOCK';
  }
  
  export interface FraudPattern {
    type: string;
    description: string;
    amount: string;
    detection: string;
  }
  
  export interface StatsData {
    totalTransactions: number;
    fraudDetected: number;
    moneySaved: string;
    avgResponseTime: string;
  }
  
  export interface RiskTrendData {
    time: string;
    risk: number;
    transactions: number;
    fraud: number;
  }
  
  export interface FraudTypeData {
    type: string;
    count: number;
    amount: string;
  }
  
  export interface PerformanceMetrics {
    accuracy: number;
    precision: number;
    recall: number;
    falsePositiveRate: number;
    avgProcessingTime: number;
    models: Array<{
      name: string;
      accuracy: number;
      precision: number;
    }>;
  }
  
  export interface GeographicHotspot {
    location: string;
    riskLevel: 'Low' | 'Medium' | 'High';
    fraudCount: number;
    trend: 'increasing' | 'decreasing' | 'stable';
  }
  
  export interface RegulatoryAlert {
    id: string;
    title: string;
    description: string;
    severity: 'low' | 'medium' | 'high';
    date: string;
  }
  
  export interface SHAPExplanation {
    transactionId: string;
    features: Array<{
      name: string;
      contribution: number;
      value: unknown;
    }>;
    summary: string;
  }
  
  export interface NetworkData {
    nodes: Array<{
      id: string;
      type: string;
      risk: string;
      amount: string;
    }>;
    links: Array<{
      source: string;
      target: string;
      amount: string;
      time: string;
    }>;
  }