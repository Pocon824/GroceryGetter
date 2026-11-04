import { Pipe, PipeTransform } from '@angular/core';

type StoreKey = 'nofrills' | 'walmart' | 'foodbasics';

const STORE_NAMES: Record<StoreKey, string> = {
  nofrills: 'No Frills',
  walmart: 'Walmart',
  foodbasics: 'Food Basics',
};

@Pipe({
  name: 'storeName',
})
export class StoreNamePipe implements PipeTransform {
  transform(value: string | null): string | null {

    if (value === null) {
      return 'No store name available';
    }
    else if (value in STORE_NAMES) {
      return STORE_NAMES[value as StoreKey];
    }

    return value;

  }
}
