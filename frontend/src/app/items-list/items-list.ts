import { Component, inject } from '@angular/core';
import {Items} from '../items';
import { toSignal } from '@angular/core/rxjs-interop';
import { CurrencyPipe } from '@angular/common';
import { StoreNamePipe } from '../store-name-pipe';

@Component({
  imports: [CurrencyPipe, StoreNamePipe],
  selector: 'app-items-list',
  styleUrl: './items-list.css',
  templateUrl: './items-list.html',
})
export class ItemsList {
  private readonly itemsService = inject(Items);

  protected readonly items = toSignal(this.itemsService.getItems());
}
