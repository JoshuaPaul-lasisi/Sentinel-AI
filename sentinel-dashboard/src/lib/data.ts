import type { Transaction, FraudPattern, StatsData } from "@interfaces/index";

export const mockTransactions: Transaction[] = [
  {
    id: "TX_001",
    amount: 150000,
    user_id: "USER_789012",
    timestamp: "2024-01-15T10:30:00Z",
    device_id: "DEV_7A3B9C",
    location: "Lagos, VI",
    bvn_age_hours: 2,
    risk_score: 0.94,
    status: "BLOCKED",
    type: "BVN Enrollment Attack",
  },
  {
    id: "TX_002",
    amount: 98000,
    user_id: "USER_345678",
    timestamp: "2024-01-15T11:15:00Z",
    device_id: "DEV_4D5E6F",
    location: "Abuja, Wuse",
    bvn_age_hours: 720,
    risk_score: 0.87,
    status: "REVIEW",
    type: "Money Mule",
  },
  {
    id: "TX_003",
    amount: 5000,
    user_id: "USER_901234",
    timestamp: "2024-01-15T12:00:00Z",
    device_id: "DEV_1A2B3C",
    location: "Port Harcourt",
    bvn_age_hours: 1440,
    risk_score: 0.12,
    status: "APPROVED",
    type: "Normal",
  },
  {
    id: "TX_004",
    amount: 250000,
    user_id: "USER_567890",
    timestamp: "2024-01-15T13:45:00Z",
    device_id: "DEV_8D9E0F",
    location: "Lagos, Ikeja",
    bvn_age_hours: 5,
    risk_score: 0.91,
    status: "BLOCKED",
    type: "BVN Enrollment Attack",
  },
  {
    id: "TX_005",
    amount: 45000,
    user_id: "USER_123456",
    timestamp: "2024-01-15T14:20:00Z",
    device_id: "DEV_3B4C5D",
    location: "Kano",
    bvn_age_hours: 2160,
    risk_score: 0.23,
    status: "APPROVED",
    type: "Normal",
  },
  {
    id: "TX_006",
    amount: 96000,
    user_id: "USER_789123",
    timestamp: "2024-01-15T15:10:00Z",
    device_id: "DEV_6E7F8G",
    location: "Abuja, Garki",
    bvn_age_hours: 2880,
    risk_score: 0.78,
    status: "REVIEW",
    type: "Money Mule",
  },
  {
    id: "TX_007",
    amount: 1200000,
    user_id: "USER_456789",
    timestamp: "2024-01-15T16:05:00Z",
    device_id: "DEV_9H0I1J",
    location: "Lagos, Lekki",
    bvn_age_hours: 4320,
    risk_score: 0.45,
    status: "APPROVED",
    type: "Large Transaction",
  },
  {
    id: "TX_008",
    amount: 32000,
    user_id: "USER_234567",
    timestamp: "2024-01-15T17:30:00Z",
    device_id: "DEV_2K3L4M",
    location: "Ibadan",
    bvn_age_hours: 3,
    risk_score: 0.83,
    status: "REVIEW",
    type: "BVN Enrollment Attack",
  },
  {
    id: "TX_009",
    amount: 87000,
    user_id: "USER_890123",
    timestamp: "2024-01-15T18:15:00Z",
    device_id: "DEV_5N6O7P",
    location: "Enugu",
    bvn_age_hours: 5760,
    risk_score: 0.67,
    status: "REVIEW",
    type: "Suspicious Pattern",
  },
  {
    id: "TX_010",
    amount: 15000,
    user_id: "USER_345679",
    timestamp: "2024-01-15T19:00:00Z",
    device_id: "DEV_8Q9R0S",
    location: "Benin City",
    bvn_age_hours: 7200,
    risk_score: 0.09,
    status: "APPROVED",
    type: "Normal",
  },
  {
    id: "TX_011",
    amount: 94000,
    user_id: "USER_901235",
    timestamp: "2024-01-15T20:45:00Z",
    device_id: "DEV_1T2U3V",
    location: "Kaduna",
    bvn_age_hours: 8640,
    risk_score: 0.72,
    status: "REVIEW",
    type: "Money Mule",
  },
  {
    id: "TX_012",
    amount: 180000,
    user_id: "USER_567891",
    timestamp: "2024-01-15T21:20:00Z",
    device_id: "DEV_4W5X6Y",
    location: "Lagos, Ajah",
    bvn_age_hours: 8,
    risk_score: 0.89,
    status: "BLOCKED",
    type: "BVN Enrollment Attack",
  },
  {
    id: "TX_013",
    amount: 2500,
    user_id: "USER_123457",
    timestamp: "2024-01-15T22:10:00Z",
    device_id: "DEV_7Z8A9B",
    location: "Abuja, Maitama",
    bvn_age_hours: 10080,
    risk_score: 0.05,
    status: "APPROVED",
    type: "Normal",
  },
  {
    id: "TX_014",
    amount: 125000,
    user_id: "USER_789124",
    timestamp: "2024-01-15T23:05:00Z",
    device_id: "DEV_0C1D2E",
    location: "Port Harcourt",
    bvn_age_hours: 11520,
    risk_score: 0.34,
    status: "APPROVED",
    type: "Normal",
  },
  {
    id: "TX_015",
    amount: 99000,
    user_id: "USER_456790",
    timestamp: "2024-01-16T00:30:00Z",
    device_id: "DEV_3F4G5H",
    location: "Lagos, Yaba",
    bvn_age_hours: 12960,
    risk_score: 0.81,
    status: "REVIEW",
    type: "Money Mule",
  },
];

export const fraudPatterns: FraudPattern[] = [
  {
    type: "Money Mule Networks",
    description:
      "Circular transaction flows with consistent fee decay patterns",
    amount: "₦100K → ₦98K → ₦96K → ₦94K",
    detection:
      "Graph intelligence identifies circular flows and fee decay chains",
  },
  {
    type: "BVN Enrollment Attacks",
    description: "Fraudulent transactions within 24 hours of BVN registration",
    amount: "₦329M stolen in 2024",
    detection: "Behavioral time-window monitoring and velocity checks",
  },
  {
    type: "Agent Collusion Networks",
    description:
      "Unusual fund cycling among banking agents in coordinated patterns",
    amount: "₦45-75M monthly",
    detection:
      "Graph reveals abnormal sub-agent linkages and transaction clusters",
  },
  {
    type: "USSD/SIM Swap Exploitation",
    description: "Unauthorized transactions via USSD without OTP verification",
    amount: "43% of mobile fraud",
    detection: "Device fingerprinting and behavioral biometrics",
  },
  {
    type: "Betting Platform Money Laundering",
    description:
      "Rapid cycling through betting platforms to clean illicit funds",
    amount: "₦12-18M weekly",
    detection: "Temporal pattern analysis and destination monitoring",
  },
  {
    type: "Salary Advance Exploitation",
    description:
      "Multiple salary advance applications across different institutions",
    amount: "₦28M detected monthly",
    detection: "Cross-institutional application monitoring",
  },
];

export const statsData: StatsData = {
  totalTransactions: 12457,
  fraudDetected: 89,
  moneySaved: "₦186.5M",
  avgResponseTime: "0.8s",
};

// Additional data for charts and analytics
export const riskTrendData = [
  { time: "00:00", risk: 8, transactions: 23, fraud: 1 },
  { time: "02:00", risk: 6, transactions: 18, fraud: 0 },
  { time: "04:00", risk: 5, transactions: 12, fraud: 0 },
  { time: "06:00", risk: 12, transactions: 45, fraud: 2 },
  { time: "08:00", risk: 18, transactions: 89, fraud: 3 },
  { time: "10:00", risk: 25, transactions: 156, fraud: 5 },
  { time: "12:00", risk: 32, transactions: 234, fraud: 8 },
  { time: "14:00", risk: 28, transactions: 198, fraud: 6 },
  { time: "16:00", risk: 35, transactions: 267, fraud: 9 },
  { time: "18:00", risk: 22, transactions: 145, fraud: 4 },
  { time: "20:00", risk: 19, transactions: 112, fraud: 3 },
  { time: "22:00", risk: 14, transactions: 67, fraud: 2 },
];

export const fraudByType = [
  { type: "BVN Attacks", count: 34, amount: "₦89.2M" },
  { type: "Money Mules", count: 28, amount: "₦45.6M" },
  { type: "Agent Collusion", count: 15, amount: "₦32.1M" },
  { type: "USSD/SIM Swap", count: 8, amount: "₦12.8M" },
  { type: "Betting Laundering", count: 4, amount: "₦6.8M" },
];

export const performanceMetrics = {
  accuracy: 96.4,
  precision: 94.2,
  recall: 92.8,
  falsePositiveRate: 3.2,
  avgProcessingTime: 0.8,
  models: [
    { name: "Isolation Forest", accuracy: 95.2, precision: 93.1 },
    { name: "Behavioral Autoencoder", accuracy: 96.4, precision: 94.2 },
    { name: "Graph Neural Network", accuracy: 97.1, precision: 95.8 },
  ],
};

export const geographicHotspots = [
  {
    location: "Lagos, VI",
    riskLevel: "High",
    fraudCount: 23,
    trend: "increasing",
  },
  {
    location: "Abuja, Wuse",
    riskLevel: "High",
    fraudCount: 18,
    trend: "stable",
  },
  {
    location: "Port Harcourt",
    riskLevel: "Medium",
    fraudCount: 12,
    trend: "increasing",
  },
  { location: "Kano", riskLevel: "Medium", fraudCount: 8, trend: "decreasing" },
  {
    location: "Lagos, Lekki",
    riskLevel: "High",
    fraudCount: 15,
    trend: "increasing",
  },
  { location: "Ibadan", riskLevel: "Low", fraudCount: 4, trend: "stable" },
];

export const regulatoryAlerts = [
  {
    id: "REG_001",
    title: "CBN AI/AML Directive",
    description:
      "New mandate for AI-driven AML solutions with NDPA 2023 explainability requirements",
    severity: "high",
    date: "2024-01-10",
  },
  {
    id: "REG_002",
    title: "NDPA Compliance Update",
    description:
      "Enhanced data protection requirements for financial AI systems",
    severity: "medium",
    date: "2024-01-08",
  },
  {
    id: "REG_003",
    title: "Fraud Reporting Framework",
    description: "Updated reporting timelines for suspected fraud cases",
    severity: "medium",
    date: "2024-01-05",
  },
];

// Mock data for SHAP explanations
export const shapExplanations = [
  {
    transactionId: "TX_001",
    features: [
      { name: "BVN Age (2 hours)", contribution: 0.45, value: "2h" },
      { name: "Transaction Amount", contribution: 0.28, value: "₦150,000" },
      { name: "Device Mismatch", contribution: 0.15, value: "Yes" },
      { name: "Location Anomaly", contribution: 0.08, value: "High" },
      { name: "Time of Day", contribution: 0.04, value: "Normal" },
    ],
    summary:
      "This transaction shows strong signs of BVN enrollment attack - occurring just 2 hours after BVN registration with unusually high amount.",
  },
  {
    transactionId: "TX_002",
    features: [
      { name: "Amount Pattern", contribution: 0.38, value: "₦98,000" },
      { name: "Recipient History", contribution: 0.27, value: "High Risk" },
      { name: "Transaction Velocity", contribution: 0.18, value: "Abnormal" },
      { name: "Geographic Distance", contribution: 0.12, value: "500km" },
      { name: "Time Since Last TX", contribution: 0.05, value: "2min" },
    ],
    summary:
      "Consistent with money mule patterns - rapid transfer to known high-risk account with fee decay amount.",
  },
];

// Network graph data for visualization
export const networkData = {
  nodes: [
    { id: "A", type: "source", risk: "high", amount: "₦150K" },
    { id: "B", type: "mule", risk: "medium", amount: "₦98K" },
    { id: "C", type: "mule", risk: "medium", amount: "₦96K" },
    { id: "D", type: "destination", risk: "high", amount: "₦94K" },
    { id: "E", type: "suspicious", risk: "low", amount: "₦45K" },
  ],
  links: [
    { source: "A", target: "B", amount: "₦150K", time: "10:30" },
    { source: "B", target: "C", amount: "₦98K", time: "10:32" },
    { source: "C", target: "D", amount: "₦96K", time: "10:34" },
    { source: "A", target: "E", amount: "₦45K", time: "10:31" },
  ],
};
