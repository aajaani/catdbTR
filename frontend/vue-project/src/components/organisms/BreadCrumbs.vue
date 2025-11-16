<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { getBreadcrumbs } from "@/router/helpers.js";

const router = useRouter();

const props = defineProps<{
	slugs?: { [ key: string ]: string }
}>( );

const entries = computed( ( ) => {
	const bcs = getBreadcrumbs( router.currentRoute.value.meta ).map( b => ({ ...b }) );
	console.log( "breadcroombss: ", bcs )

	if ( props.slugs ) {
		for ( let i = 0; i < bcs.length; i++ ) {
			if ( !bcs[ i ] ) continue;

			Object.entries( props.slugs ).forEach( ([ slug, value ]) => {
				console.log( slug, value )
				// @ts-ignore
				bcs[ i ].name = bcs[ i ].name.replaceAll( `{${slug}}`, value );
				console.log( bcs[ i ] )
			} );
		}
	}

	return bcs;
} );
</script>

<template>
	<nav aria-label="Breadcrumb" v-if="entries.length > 0 && entries">
		<ol class="flex items-center gap-2" id="breadcrumbs">
			<li v-for="( entry, i ) in entries" :key="i"
				class="flex items-center gap-2 breadcrumb abril-fatface-regular">
				<!-- first entries are less opaque than the last one -->
				<router-link
					v-if="entry.link"
					:to="entry.link"
				>
					{{ entry.name }}
				</router-link>

				<span v-else>
				  {{ entry.name }}
				</span>
			</li>
		</ol>
	</nav>
</template>

<style scoped>
nav {
	--bc-active: theme("colors.breadcrumbs.active");
	--bc-inactive: theme("colors.breadcrumbs.inactive");

	&.light {
		/* they do exist, tailwind is going crazy */
		--bc-active: theme("colors.breadcrumbs.light.active");
		--bc-inactive: theme("colors.breadcrumbs.light.inactive");
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
		color: var(--text-muted);
	}

	a {
		color: var(--bc-inactive);
		text-decoration: none;
	}
}

.breadcrumb:last-child > * {
	color: var(--bc-active)
}
</style>