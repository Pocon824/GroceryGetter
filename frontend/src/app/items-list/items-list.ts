import { Component, inject, signal } from '@angular/core';
import {Items} from '../items';
import { toSignal, toObservable } from '@angular/core/rxjs-interop';
import { CurrencyPipe } from '@angular/common';
import { StoreNamePipe } from '../store-name-pipe';
import { switchMap } from 'rxjs/internal/operators/switchMap';

@Component({
  imports: [CurrencyPipe, StoreNamePipe],
  selector: 'app-items-list',
  styleUrl: './items-list.css',
  templateUrl: './items-list.html',
})
export class ItemsList {
  private readonly itemsService = inject(Items);

  protected readonly query = signal('');

  protected readonly items = toSignal(
    toObservable(this.query).pipe(
      switchMap((query) => this.itemsService.getItems(query))
    ),
  );

}
