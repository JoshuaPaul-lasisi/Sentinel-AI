import { Module } from '@nestjs/common';
import { GraphController } from './graph.controller';
import { GraphService } from './graph.service';
import { ConfigModule } from '@nestjs/config';


@Module({
  imports: [ConfigModule,],
  controllers: [GraphController],
  providers: [GraphService,],
  exports: [GraphService],
})
export class GraphModule {}
