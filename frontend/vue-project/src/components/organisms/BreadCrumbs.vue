<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, type RouteLocationRaw } from 'vue-router';

// breadcrumbentry should be able to be a string or a function that takes the route and returns a string
// function allows for dynamic routes like /cats/:id to return the cat's name or whatever
// link is optional, if not provided the breadcrumb will not be a link (for the current page)
interface BreadCrumbEntry {
  name: string | ( ( route: ReturnType< typeof useRoute > ) => string );
  link?: string;
}

const route = useRoute( );

// typescript is so boss
const entries = computed< BreadCrumbEntry[ ] >(( ) => {
  // no breadcrumbs defined for this route, nothing to show
  if ( !route.meta || !route.meta.breadcrumbs ) return [ ];
  return route.meta.breadcrumbs as BreadCrumbEntry[ ];
});
</script>

<template>
  <nav aria-label="Breadcrumb" v-if="entries.length > 0 && entries">
    <ol class="flex items-center gap-2" id="breadcrumbs">
      <li v-for="( entry, i ) in entries" :key="i" class="flex items-center gap-2 breadcrumb abril-fatface-regular">
        <!-- first entries are less opaque than the last one -->
        <router-link
            v-if="entry.link"
            :to="entry.link"
        >
          {{ typeof entry.name === 'function'
            // entries name could be a function that takes the route and returns a string (type also defined above)
            ? entry.name( route )
            : entry.name }}
        </router-link>
        <span v-else>
          {{ typeof entry.name === 'function'
            // entries name could be a function that takes the route and returns a string (type also defined above)
            ? entry.name( route )
            : entry.name }}
        </span>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
nav {
  --bc-active: theme( "colors.breadcrumbs.active" );
  --bc-inactive: theme( "colors.breadcrumbs.inactive" );

  &.light {
    /* they do exist, tailwind is going crazy */
    --bc-active: theme( "colors.breadcrumbs.light.active" );
    --bc-inactive: theme( "colors.breadcrumbs.light.inactive" );
  }
}

/* has next breadcrumb? */
.breadcrumb:has( + .breadcrumb ) {
  padding-right: 1rem;
  position: relative;
  &:has( > a ):hover {
    text-decoration: underline;
  }

  /* absolute, otherwise gets underlined on link hover */
  &::before {
    content: "/";
    position: absolute;
    right: 0;
    color: var( --text-muted );
  }

  a {
    color: var( --bc-inactive );
    text-decoration: none;
  }
}

.breadcrumb:last-child > * {
  color: var( --bc-active )
}
</style>