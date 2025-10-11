<script setup lang="ts">
import { MdFeed, MdOutlinePets, MdCatchingPokemon, MdPersonAdd, MdPeople, MdArrowBack } from 'vue-icons-plus/md'
import { useRoute } from 'vue-router';

// reactive route
const route = useRoute( );


// todo: add translations, idk if i18n exists for vue3
const sidebar_links = {
  "/": {
    title: "Ulevaade",
    icon: MdFeed,
  },
  "/cats": {
    title: "Kassid",
    icon: MdOutlinePets,
  },
  "/add-cat": {
    title: "Lisa kass",
    icon: MdCatchingPokemon,
  },
  "/add-manager": {
    title: "Lisa hooldaja",
    icon: MdPersonAdd,
  },
  "/personal": {
    title: "Personal",
    icon: MdPeople,
  }
}
</script>

<template>
<aside class="flex flex-col gap-6 pt-4">
  <div class="pl-4 flex flex-row justify-between">
    <h1 class="poppins-medium text-[18px] text-nav-li-text">Kassid Koju</h1>

    <!-- todo: figure out if this is back or collapse -->
    <span id="collapse" class="relative translate-x-[50%] w-[40px] aspect-square h-auto left-0 p-2 bg-nav-li-text self-end justify-self-end flex place-items-center justify-center rounded-[8px]">
      <MdArrowBack size="20" class="fill-nav-bg bg-main-bg"/>
    </span>
  </div>
  <div class="profile-container flex gap-4 px-4">
    <!--  images cant have pseudo elements (for status), need a wrapper  -->
    <span data-status="online" class="profile-picture-container w-[42px] h-[42px] rounded-md relative">
      <img class="h-max rounded-md" alt="profile picture" src="https://picsum.photos/50/50"/>
    </span>
    <div class="flex flex-col text-[var(--nav-li-text)]">
      <h2 class="text-inherit poppins-medium text-[14px]">Kassi admin1</h2>
      <p class="poppins-regular text-[11px]">Admin</p>
    </div>
  </div>

  <nav>
    <ul class="flex flex-col color-nav-li-text pl-14">
      <!-- link items come from script setup -->
      <li
        v-for="(link, path) in sidebar_links"
        :key="path"
        :data-active="route.path === path ? 'true' : 'false'"
        class="nav-item"
      >
        <router-link :to="path" class="nav-link grid pr-9 rounded-l-3xl pl-6 py-2">
          <span class="flex gap-4 inactive">
            <component :is="link.icon" size="36" class="fill-inherit" />
            <span class="poppins-medium text-[14px] color-inherit">{{ link.title }}</span>
          </span>

          <span class="flex gap-4 active">
            <component :is="link.icon" size="36" class="fill-inherit" />
            <span class="poppins-medium text-[14px] color-inherit">{{ link.title }}</span>
          </span>
        </router-link>
      </li>
    </ul>
  </nav>
</aside>
</template>

<style scoped>
aside {
  background: var( --nav-li-bg );

  /* would have global x padding but list items wouldn't be able to "connect" with the page */
}

li.nav-item {
  @apply py-3;
  color: var( --nav-li-text );
  fill: var( --nav-li-icon );

  --transition-duration: 200ms;

  /* new stacking context for pseudoel */
  position: relative;
  z-index: 0;

  /* hide pseudoelements when out of view */
  overflow: hidden;


  /* place children ontop of eachother */
  & .nav-link > * {
    grid-row: 1;
    grid-column: 1;
  }

  /* active/inactive */
  & .nav-link > span {
    &:is( .inactive ) {
      color: var( --nav-li-text );
      fill: var( --nav-li-icon );
      clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
    }

    &:is( .active ) {
      color: var( --nav-li-selected-text );
      fill: var( --nav-li-selected-icon );
      clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
    }

    transition: clip-path var( --transition-duration ) ease;
    align-items: center;
  }

  /* right now the selected text
     is the same as normal and blends
     in with the background
     
     because we use an absolute pseudoelement
     we cant set <a>'s blending mode to
     difference as it would use the
     navbar background as a reference (i think)

     another idea would be to use clip,
     then stack link inner text on top
     (would mean we have to duplicate link text)
     and then we can animate a clip kind of
     the same way as we animate ::before's bg
  */

  & a {
    position: relative;
    z-index: 0;
  }

  & a::before {
    content: "";
    position: absolute;
    background: var( --nav-li-selected );
    transition: translate var( --transition-duration ) ease;
    inset: 0;
    width: 100%;
    height: 100%;
    transform: 0 0;
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;

    /* move behind parent */
    z-index: -1;
  }

  /* move next bg to active */
  /* todo: background has to be relative to li's, otherwise
           animating between multiple children will introduce
           artifacts behind inbetween children
  */
  &[data-active="true"] ~ .nav-item a::before {
    translate: 0 -150%;
  }

  &[data-active="true"] ~ .nav-item .nav-link .active {
      clip-path: polygon( 0 -100%, 100% -100%, 100% 0%, 0 0% );
  }

  /* move top link to active */
  &:has( ~ .nav-item[data-active="true"] ) a::before {
    translate: 0 150%;
  }

  &:has( ~ .nav-item[data-active="true"] ) .nav-link .active {
    clip-path: polygon( 0 100%, 100% 100%, 100% 200%, 0 200% );
  }
}


.profile-picture-container {
  --status-color: #aaa; /* default to offline */
}

.profile-picture-container[data-status="online"] {
  --status-color: #2ED47A;
}

.profile-picture-container::after {
  content: "";
  position: absolute;
  bottom: 0;
  right: 0;
  transform: translateX( 50% ) translateY( -30% );

  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid var( --nav-li-bg );
  background-color: var( --status-color );
}
</style>