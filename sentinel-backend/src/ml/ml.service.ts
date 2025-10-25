import { Injectable } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { lastValueFrom } from 'rxjs';

@Injectable()
export class MlService {
  private baseUrl: string;
  constructor(
    private readonly http: HttpService,
    private readonly config: ConfigService,
  ) {
    this.baseUrl = this.config.get<string>('ML_API_URL') as string;
  }

  async predict(transactionData: any) {
    const response = await lastValueFrom(
      this.http.post(this.baseUrl, transactionData),
    );
    return response.data;
  }
}
