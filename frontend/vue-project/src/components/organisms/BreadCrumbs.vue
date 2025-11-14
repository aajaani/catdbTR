<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { getBreadcrumbs } from "@/router/helpers.js";

const router = useRouter();

// typescript is so boss
const entries = computed( () => {
	// no breadcrumbs defined for this route, nothing to show
	return getBreadcrumbs( router.currentRoute.value.meta )
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