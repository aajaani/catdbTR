/*
    type """generator"""" for filterTable, better inlay hints
*/

import type { ComponentProps, } from "vue-component-type-helpers";
import type { Prettify } from "@/type_utils.ts";
import {type Component, markRaw, type Raw, type Ref, ref} from "vue";


export interface OptionAsComponent<Component> {
    component: Component,
    props: ComponentProps< Component >,
    searchName: string
}

export type filterInputOptionsType<T> = string[ ] | OptionAsComponent<T>[ ] | ( ( ) => Promise< string[ ] > )
export type filterInputOptionType<T> = string | OptionAsComponent<T>

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
    //  search: just a keyword to filter
    //  toggle: buttongroup input based on unique groups from given values OR custom values to show in input 
    filterMode?: "unique" | "search" | "toggle",
    // unique -> status, manager name
    // search -> cat name, status
    // toggle -> on homepage
    // todo: have to think of a way to support searching by colonies, would use unique

    // only exists on filterMode=unique & toggle, groups to show in search
    filterInputOptions?: filterInputOptionsType< ComponentType >,
    
    // todo: rethink if we need this, would be useful for filtering for "on homepage"
    //       "yes" / "no" -> mapped visible in this fn based on selected opt
    filterFn?: ( props: ComponentProps< ComponentType >, keywords: string[ ] ) => boolean,

    // styling vars
    centerEntries?: boolean,
    // should min width be content length
    fitContent?: boolean,
    centerTitle?: boolean
}

// field converts TableField component to raw (vue is not happy about nested reactivity)
type FieldReturn< C extends Component > = TableField< C > & { component: Raw< C > };
export type FieldsMap = Record< string, FieldReturn< Component > >;

export type RowEntry< F extends Record< string, FieldReturn< Component > > > = {
    [ K in keyof F ]: ComponentProps< F[ K ][ "component" ] >
}

// wrapper to create tables<br>
// intention: have defined type hints for filter and sort functions
export const field = < C extends Component >( def: TableField< C > ) => ({ ...def, component: markRaw( def.component ) }) as FieldReturn< C >;


type TableFilterModel< F > = {
    filters: { [ key in keyof F ]?: string[ ] }
}

export type TableFilterModelWeak = {
    filters: { [ key: string ]: string[ ] }
}

// explanation:
// > F extends FieldsMap (Record<string, FieldReturn< Component >)
// give us type hints if anything is missing from component props that is required
// tried to prettify type errors but no solution for that yet
//
// FieldReturn is created so we can mark each component in fields (table head)
// as raw (vue was yelling, found that to be the fix), also what `field` function returns
//
// for entries, type is typed to let us know when some prop is missing from a component
// for example, has to match RowEntry< FieldReturn + component (now raw, handled by field function)
// RowEntry unions component props to each field return (let ts let us know when a property that's needed is missing)
export function defineTable< F extends Record< string, Prettify< FieldReturn< Component > > > >(
    fields: F,
    entries: RowEntry< F >[ ]
) {
    return { fields, entries } as const;
}

export function defineTableModel< F extends Record< string, Prettify< FieldReturn< Component > > > >( ): Ref<TableFilterModel< F >> {
    return ref({
        filters: { }
    })
}