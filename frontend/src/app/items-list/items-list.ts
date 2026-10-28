import { Component } from '@angular/core';
import { CurrencyPipe } from '@angular/common';

interface Item {
  id: number;
  name: string;
  price: number;
}

@Component({
  imports: [CurrencyPipe],
  selector: 'app-items-list',
  styleUrl: './items-list.css',
  templateUrl: './items-list.html',
})
export class ItemsList {
  protected readonly items: Item[] = [
    { id: 1, name: 'Chicken thighs, bone in', price: 9.83 },
    { id: 2, name: 'Butter, salted', price: 5.99 },
    { id: 3, name: 'Bananas', price: 1.75 },
  ];
}
