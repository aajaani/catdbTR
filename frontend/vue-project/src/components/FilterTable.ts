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

    // -1 0 1, toLocaleCompare on strings for example, same result type
    sortFn?: ( props1: ComponentProps< ComponentType >, props2: ComponentProps< ComponentType > ) => number;
    disableSorting?: boolean,

    // what should be filterable?
    //  unique: creates unique groups from given values OR custom values to show in filter input 
    //  search: just a keyword to filter with
    //  toggle: buttongroup input based on unique groups from given values OR custom values to show in input 
    filterMode?: "unique" | "search" | "toggle",
    // unique -> status, manager name
    // search -> cat name, status
    // toggle -> on homepage
    // todo: have to think of a way to support searching by colonies, would use unique but how would we account for

    // only exists on filterMode=unique, groups to show in search
    filterInputOptions?: string[ ],
    
    // todo: rethink if we need this, would be useful for filtering for "on homepage"
    //       "yes" / "no" -> mapped visible in this fn based on selected opt
    filterFn?: ( fieldValues: string[ ] ) => boolean,

    // styling vars
    centerEntries?: boolean,
    // should min width be content length
    fitContent?: boolean,
    centerTitle?: boolean
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