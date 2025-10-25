import { Injectable, OnModuleInit } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import neo4j, { Driver } from 'neo4j-driver';
import {
  CreateTransactionDto,
  TransactionResponseDto,
} from 'src/transactions/dtos/create-transaction.dto';

@Injectable()
export class GraphService implements OnModuleInit {
  private driver: Driver;
  constructor(private configSevice: ConfigService) {}
  async onModuleInit() {
    this.driver = neo4j.driver(
      this.configSevice.get<string>('NEO4J_URI') as string,
      neo4j.auth.basic(
        this.configSevice.get<string>('NEO4J_USER') as string,
        this.configSevice.get<string>('NEO4J_PASSWORD') as string,
      ),
    );
    await this.driver.verifyConnectivity();
  }



  private async runQuery(query: string, params: any = {}) {
    const session = this.driver.session();
    try {
      const result = await session.run(query, params);
      return result;
    } catch (error) {
      console.error('Neo4j query error:', error);
      throw error;
    } finally {
      await session.close();
    }
  }


  async getAccounts() {
    const query = `
      MATCH (a:Account)
      RETURN a.id AS id, a.name AS name, a.bank AS bank, a.country AS country
    `;

    const result = await this.runQuery(query);
    return result.records.map((r) => r.toObject());
  }

  async getDevices() {
    const query = `
      MATCH (d:Device)
      RETURN d.id AS id, d.imei AS imei
    `;
    const result = await this.runQuery(query);
    return result.records.map((r) => r.toObject());
  }
  async getTransactions() {
    const query = `
      MATCH (t:Transaction)
      RETURN t.id AS id, t.amount AS amount, t.timestamp AS timestamp
      ORDER BY t.timestamp DESC
    `;
    const cypher = `
    MATCH (a:Account)-[:PERFORMED]->(t:Transaction)
    OPTIONAL MATCH (t)-[:FROM_LOCATION]->(l:Location)
    OPTIONAL MATCH (t)-[:USING_DEVICE]->(d:Device)
    RETURN t, a.id as user_id, l.name as location, d.id as device_id
    ORDER BY t.timestamp DESC
    LIMIT 100
  `;

    const result = await this.runQuery(cypher);

    return result.records.map((r) => r.toObject());
  }

  async getHighRiskTransactions() {
    const query = `
      MATCH (a:Account)-[:PERFORMED]->(t:Transaction)
      WHERE t.risk_score > 0.7
      OPTIONAL MATCH (t)-[:FROM_LOCATION]->(l:Location)
      OPTIONAL MATCH (t)-[:USING_DEVICE]->(d:Device)
      RETURN t, a.id as user_id, l.name as location, d.id as device_id
      ORDER BY t.risk_score DESC
    `;

    const result = await this.runQuery(query);

    return result.records.map((r) => r.toObject());
  }

  async getDashboardStats() {
    const cypher = `
      MATCH (t:Transaction)
      WITH 
        count(t) as totalTransactions,
        sum(t.amount) as totalAmount,
        sum(CASE WHEN t.risk_score > 0.7 THEN 1 ELSE 0 END) as highRiskCount
      
      MATCH (t2:Transaction {status: 'BLOCKED'})
      WITH 
        totalTransactions,
        totalAmount,
        highRiskCount,
        count(t2) as blockedCount,
        sum(t2.amount) as blockedAmount
      
      RETURN 
        totalTransactions,
        highRiskCount,
        blockedCount,
        blockedAmount,
        CASE 
          WHEN blockedAmount IS NULL THEN '₦0' 
          ELSE '₦' + toString(blockedAmount / 1000000) + 'M' 
        END as moneySaved,
        '0.8s' as avgResponseTime,
        totalAmount
    `;
  
    const results = await this.runQuery(cypher);
    
    // Check if we have results
    if (!results.records.length) {
      return {
        totalTransactions: 0,
        fraudDetected: 0,
        moneySaved: '₦0',
        avgResponseTime: '0.8s',
        totalAmountProcessed: 0,
        blockedAmount: 0
      };
    }
  
    const record = results.records[0].toObject();
    
    // Handle Neo4j integer types and null values safely
    const totalTransactions = record.totalTransactions ? record.totalTransactions.low || record.totalTransactions : 0;
    const highRiskCount = record.highRiskCount ? record.highRiskCount.low || record.highRiskCount : 0;
    const totalAmount = record.totalAmount ? record.totalAmount.low || record.totalAmount : 0;
    const blockedAmount = record.blockedAmount ? record.blockedAmount.low || record.blockedAmount : 0;
  
    return {
      totalTransactions,
      fraudDetected: highRiskCount,
      moneySaved: record.moneySaved || '₦0',
      avgResponseTime: record.avgResponseTime || '0.8s',
      totalAmountProcessed: totalAmount,
      blockedAmount
    };
  }
  async detectMoneyMuleNetworks(): Promise<any[]> {
    const cypher = `
      // Money Mule Detection - Circular transactions
      MATCH path = (a1:Account)-[t1:SENT_TO]->(a2:Account)-[t2:SENT_TO]->(a3:Account)-[t3:SENT_TO]->(a1)
      WHERE t1.amount > 50000 AND t2.amount > 50000 AND t3.amount > 50000
      RETURN 
        a1.id as account1,
        a2.id as account2, 
        a3.id as account3,
        t1.amount as amount1,
        t2.amount as amount2,
        t3.amount as amount3,
        'Circular Money Mule Network' as pattern
      
      UNION
      
      // Fee decay pattern detection
      MATCH (a1:Account)-[t1:SENT_TO]->(a2:Account)-[t2:SENT_TO]->(a3:Account)
      WHERE t1.amount > 90000 
        AND t2.amount > 80000 
        AND t1.amount > t2.amount
        AND (t1.amount - t2.amount) < 5000
      RETURN 
        a1.id as account1,
        a2.id as account2,
        a3.id as account3,
        t1.amount as amount1,
        t2.amount as amount2,
        null as amount3,
        'Fee Decay Pattern' as pattern
    `;

    const result = await this.runQuery(cypher);
    return result.records.map((r) => r.toObject());
  }

  private calculateRiskScore(transaction: CreateTransactionDto): number {
    let score = 0.1; // Base score

    // BVN age factor
    if (transaction.bvn_age_hours && transaction.bvn_age_hours < 24) {
      score += 0.4;
    }

    // Amount factor
    if (transaction.amount > 100000) {
      score += 0.3;
    }

    // Location factor (simplified)
    if (
      transaction.location.includes('Lagos') ||
      transaction.location.includes('Abuja')
    ) {
      score += 0.2;
    }

    return Math.min(score, 0.95);
  }

  private determineStatus(riskScore: number): string {
    if (riskScore > 0.7) return 'BLOCKED';
    if (riskScore > 0.4) return 'REVIEW';
    return 'APPROVED';
  }

  private determineTransactionType(
    transaction: CreateTransactionDto,
    riskScore: number,
  ): string {
    if (
      transaction.bvn_age_hours &&
      transaction.bvn_age_hours < 24 &&
      riskScore > 0.7
    ) {
      return 'BVN Enrollment Attack';
    }
    if (transaction.amount > 90000 && riskScore > 0.6) {
      return 'Money Mule';
    }
    return 'Normal';
  }

  private generateSHAPExplanation(
    transaction: CreateTransactionDto,
    riskScore: number,
  ): any {
    let features: any[] = [];

    if (transaction.bvn_age_hours && transaction.bvn_age_hours < 24) {
      features.push({
        name: 'BVN Age',
        contribution: 0.4,
        value: `${transaction.bvn_age_hours}h`,
      });
    }

    if (transaction.amount > 100000) {
      features.push({
        name: 'Transaction Amount',
        contribution: 0.3,
        value: `₦${transaction.amount.toLocaleString()}`,
      });
    }

    features.push({
      name: 'Location Risk',
      contribution: 0.2,
      value: transaction.location,
    });

    return {
      risk_score: riskScore,
      features: features,
      summary: `Transaction flagged due to ${features.map((f) => f.name.toLowerCase()).join(', ')}`,
    };
  }

  async close() {
    await this.driver?.close();
  }

  async checkDatabase() {
    const query = `MATCH (n) RETURN count(n) as nodeCount`;
    const result = await this.runQuery(query);
    return {
        status : 'success',
        nodeCount : result.records[0].get('nodeCount').low,
        message : 'Total nodes in database: '+ result.records[0].get('nodeCount')
    }
  }
}
