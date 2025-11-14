// function allows for dynamic routes like /cats/:id to return the cat's name or whatever
// link is optional, if not provided the breadcrumb will not be a link (for the current page)
interface Breadcrumb {
	name: string,
	link?: string
}

export function defineBreadcrumbs( ...breadcrumbs: Breadcrumb[] ) {
	return { breadcrumbs: [ ...breadcrumbs ] };
}

export function defineSidebar( enabled: boolean ) {
	return { sidebar: enabled };
}

export function getBreadcrumbs( routeMeta: any ): Breadcrumb[] {
	if ( routeMeta && routeMeta.breadcrumbs ) {
		return routeMeta.breadcrumbs as Breadcrumb[];
	}

	return [];
}

export function setBreadcrumb( routemeta: any, index: number, newName: string ) {
    // aaaa if we set directly breaks everything
    const bc = [ ...getBreadcrumbs( routemeta ) ];

    if ( index < 0 )
        index = bc.length + index;

    if ( !bc[ index ] ) return bc;

    // @ts-ignore we check for breadcrumb validity, why is ts unhappy?
    bc[ index ].name = newName;

    return bc;
}

export function isSidebarAvailable( routeMeta: any ): boolean {
	if ( routeMeta && typeof routeMeta.sidebar === "boolean" ) {
		return routeMeta.sidebar as boolean;
	}

	return false;
}