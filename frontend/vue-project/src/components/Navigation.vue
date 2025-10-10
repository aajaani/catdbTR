<script setup lang="ts">
import { MdFeed, MdOutlinePets, MdCatchingPokemon, MdPersonAdd, MdPeople, MdArrowBack } from 'vue-icons-plus/md'
import router from "@/router/index.js";

const active_route = router.currentRoute.value.path;

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
      <li v-for="(link, path) in sidebar_links" :key="path" :data-active="active_route === path ? '' : null" class="nav-item pr-5 rounded-l-3xl">
        <router-link :to="path" class="nav-li flex items-center gap-4 pr-4 pl-6 py-2">
          <component :is="link.icon" size="36" class="fill-inherit" />
          <span class="poppins-medium text-[14px] color-inherit">{{ link.title }}</span>
        </router-link>
      </li>
    </ul>
  </nav>
</aside>
</template>

<style scoped>
aside {
  background: var( --nav-li-bg );

  /* would have global padding but list items wouldn't be able to "connect" with the page */
}

li.nav-item {
  @apply my-3;
  transition: background 0.3s, color 0.3s;
  background: var( --nav-li-bg );
  color: var( --nav-li-text );
  fill: var( --nav-li-icon );
  &[data-active=""] {
    background: var( --nav-li-selected );
    color: var( --nav-li-selected-text );
    fill: var( --nav-li-selected-icon );
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