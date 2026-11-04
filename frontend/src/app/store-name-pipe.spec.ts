import { StoreNamePipe } from './store-name-pipe';

describe('StoreNamePipe', () => {
  it('create an instance', () => {
    const pipe = new StoreNamePipe();
    expect(pipe).toBeTruthy();
  });
});

describe('storeNamePipe', () => {
    it('should transform foodbasics to Food Basics', () => {
    const pipe = new StoreNamePipe();
    const storeName = 'foodbasics';
    const transformedName = pipe.transform(storeName);
    expect(transformedName).toBe('Food Basics');
  });
});
