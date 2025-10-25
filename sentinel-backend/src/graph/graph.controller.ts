import { Controller, Get } from '@nestjs/common';
import { GraphService } from './graph.service';

@Controller('graph')
export class GraphController {
  constructor(private readonly graphService: GraphService) {}



  @Get('accounts')
  getAccounts() {
    return this.graphService.getAccounts();
  }

  @Get('devices')
  getDevices() {
    return this.graphService.getDevices();
  }

  @Get('transactions')
  getTransactions() {
    return this.graphService.getTransactions();
  }
  @Get('transactions/high-risk')
  highRiskTransactions() {
    return this.graphService.getHighRiskTransactions();
  }


  @Get('stats')
  async getDashboardStats() {
    return this.graphService.getDashboardStats();
  }

  @Get('money-mules')
  async detectMoneyMuleNetworks() {
    return this.graphService.detectMoneyMuleNetworks();
  }
  @Get('check-database')
  async checkDataBase() {
    return this.graphService.checkDatabase();
  }
}
