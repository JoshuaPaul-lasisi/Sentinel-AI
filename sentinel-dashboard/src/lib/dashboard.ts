import { apiClient } from "./api";

export interface Transaction {
  id: string;
  amount: number;
  user_id: string;
  timestamp: string;
  device_id: string;
  location: string;
  bvn_age_hours?: number;
  risk_score: number;
  status: "APPROVED" | "REVIEW" | "BLOCKED";
  type: string;
  ml_explanation?: any;
}

export interface CreateTransactionDto {
  amount: number;
  user_id: string;
  device_id: string;
  location: string;
  bvn_age_hours?: number;
}

export interface StatsResponse {
  totalTransactions: number;
  fraudDetected: number;
  moneySaved: string;
  avgResponseTime: string;
  totalAmountProcessed: number;
}

export interface FraudPattern {
  type: string;
  description: string;
  amount: string;
  detection: string;
}

export interface MoneyMuleNetwork {
  account1: string;
  account2: string;
  account3: string;
  amount1: number;
  amount2: number;
  amount3: number | null;
  pattern: string;
}

// Transaction APIs
export const transactionService = {
  // Get all transactions
  getTransactions: async (): Promise<Transaction[]> => {
    const response = await apiClient.get<Transaction[]>("/api/v1/graph/transactions");
    return response.data;
  },

  // Get high-risk transactions
  getHighRiskTransactions: async (): Promise<Transaction[]> => {
    const response = await apiClient.get<Transaction[]>(
      "/api/v1/graph/transactions/high-risk"
    );
    return response.data;
  },




  // Get dashboard statistics
  getDashboardStats: async (): Promise<StatsResponse> => {
    const response = await apiClient.get<StatsResponse>(
      "/api/v1/graph/transactions/stats"
    );
    return response.data;
  },

  // Detect money mule networks
  getMoneyMuleNetworks: async (): Promise<MoneyMuleNetwork[]> => {
    const response = await apiClient.get<MoneyMuleNetwork[]>(
      "/api/v1/graph/transactions/money-mules"
    );
    return response.data;
  },
};

// // Fraud Patterns APIs
// export const fraudPatternService = {
//   // Get all fraud patterns
//   getFraudPatterns: async (): Promise<FraudPattern[]> => {
//     const response = await apiClient.get<FraudPattern[]>("/api/v1/fraud-patterns");
//     return response.data;
//   },
// };

export const dashboardService = {
  getDashboardStats: async () => {
    const res = await apiClient.get("/api/v1/v1/graph/stats");
    return res;
  },
};
