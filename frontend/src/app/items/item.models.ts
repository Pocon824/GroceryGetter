export type UnitBasis = 'kg' | 'L' | 'each';

export interface ItemSummary {
id : number
name : string
category : string | null
observation_count : number
latest_store : string | null
latest_observed_on : string | null
latest_price : number | null
latest_unit_price : number | null
unit_basis: string | null
} export default ItemSummary;