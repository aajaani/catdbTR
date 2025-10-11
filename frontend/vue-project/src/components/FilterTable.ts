/*
    type """generator"""" for filterTable, better inlay hints
*/

import type { ComponentProps, } from "vue-component-type-helpers";

// given entry component can either be a vue component (todo: or a html tag)
export interface TableField<
    ComponentType
> {
    // text shown in table
    title: string,
    // component of table entry, table entry passes props to this component to render it with
    // would be cool if we can get the proptype from this component and apply it to the corresponding entry
    component: ComponentType,
    // idk if we can even have a sort function of alphabetic by default
    // since we expect a function which gets passed props of compared components 
    // HTMLElement should suffice to pass as proptypoe when dealing with html els (not supported atm)
    // filter returns true/false based on if it matches the query
    // q: do props update here when our component is reactive?
    // todo: arguments in these are type of unknown
    filterFn?: ( props1: ComponentProps< ComponentType > ) => boolean;
    // -1 0 1, toLocaleCompare on strings for example, same result type
    sortFn?: ( props1: ComponentProps< ComponentType >, props2: ComponentProps< ComponentType > ) => number;

    // styling vars
    centerEntries?: boolean,
    // should min width be content length
    fitContent?: boolean,
}

export type FieldsMap = Record< string, TableField< any > >;
export type RowEntry< FieldMap extends FieldsMap > = {
    [ K in keyof FieldMap ]: ComponentProps< FieldMap[ K ][ "component" ] >
}

// wrapper to create tables
// intention: have defined type hints for filter and sort functions
export const field = < C >( def: TableField< C > ) => def;

// F extends FieldsMap, ts will pick up on component and replace that for
// TableField type so that the component inside TableField gets the
// correct component type
//
// RowEntry will pick up on component from FieldMap at index K (key of itself)
// and take the given component and extract its' props
export function defineTable< F extends FieldsMap >( fields: F, entries: RowEntry< F >[ ] ) {
    return { fields, entries };
}