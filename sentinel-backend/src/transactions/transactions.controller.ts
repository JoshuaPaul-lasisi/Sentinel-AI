import { Controller, Body , Post  } from '@nestjs/common';
import { TransactionsService } from './transactions.service';
import { CreateTransactionDto } from './dtos/create-transaction.dto';

@Controller('transactions')
export class TransactionsController {
    constructor (private readonly transactionsService: TransactionsService){}
    @Post("analyze")
    analyzeTransaction (@Body() body : CreateTransactionDto){
        
        return this.transactionsService.analyzeTransaction(body);
    }
}
