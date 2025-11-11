<script setup lang="ts">
import Button from "@/components/atoms/Button.vue";
import api from "@/api_fetch.js";
import { ref } from "vue";
import { useToast } from "primevue";
import { useRouter } from "vue-router";

const router = useRouter( )

const ELoginState = {
  IDLE: "login:idle",
  LOADING: "login:loading",
  SUCCESS: "login:success",
  ERROR: "login:error"
}

// todo: browser autocomplete
const username = ref( "" );
const password = ref( "" );
const loginState = ref( ELoginState.IDLE );

const toast = useToast( )

const onSubmit = ( ) => {
  if ( loginState.value === ELoginState.LOADING ) return;
  loginState.value = ELoginState.LOADING;


  api.loginLoginPost( {
    body: {
      username: username.value,
      password: password.value
    }
  }).then( res => {
    if ( res.error ) {
      toast.add({
                   severity: 'error',
                   summary: 'Ebaõnnestus',
                   detail: 'Sisselogimine ebaõnnestus. Palun kontrollige oma kasutajanime ja parooli ning proovige uuesti.',
                   life: 3000
                 });
      loginState.value = ELoginState.ERROR;
      return;
    } else {
      if ( res.response.status !== 200 ) {
        toast.add({
                     severity: 'error',
                     summary: 'Ebaõnnestus',
                     detail: 'Sisselogimine ebaõnnestus. Palun kontrollige oma kasutajanime ja parooli ning proovige uuesti.',
                     life: 3000
                   });
        loginState.value = ELoginState.ERROR;
        return;
      }
      toast.add({ severity: 'success', summary: 'Õnnestus', detail: 'Olete edukalt sisse logitud!', life: 3000 });
      loginState.value = ELoginState.SUCCESS;

      if ( router.currentRoute.value.query?.redirect ) {
        const redirectPath = decodeURIComponent( router.currentRoute.value.query.redirect as string );
        router.push( redirectPath );
      } else {
        router.push({ name: 'Dashboard' });
      }
    }
  });
}
</script>

<template>
<div class="grid place-content-center">
  <form
    class="flex flex-col gap-2 border-solid border-[1px] border-border-group rounded-md px-4 py-2 shadow-md bg-main-bg poppins-medium"
    @submit.prevent="onSubmit"
  >
    <div class="flex flex-col">
      <label for="username" class="own-font poppins-light text-sm">E-mail</label>
      <input
          type="text"
          id="username"
          name="username"
          placeholder="E-mail"
          class="input own-font poppins-light text-sm"
          v-model="username"
          :disabled="[ ELoginState.LOADING, ELoginState.SUCCESS ].includes( loginState )"
          required />
    </div>
    <div class="flex flex-col">
      <label for="password" class="own-font poppins-light text-sm">Parool</label>
      <input
          type="password"
          id="password"
          name="password"
          placeholder="••••••"
          class="input own-font poppins-light text-sm"
          v-model="password"
          :disabled="[ ELoginState.LOADING, ELoginState.SUCCESS ].includes( loginState )"
          required />
    </div>

    <Button
        class="primary"
        type="submit"
        :disabled="[ ELoginState.LOADING, ELoginState.SUCCESS ].includes( loginState )"
    >
      <span
       v-if="loginState === ELoginState.LOADING"
       class="inline-block h-5 w-5 animate-spin rounded-full border-2 border-solid border-current border-e-transparent border-s-transparent"
      ></span>

      <span
        v-else
      >
        Logi Sisse
      </span>
    </Button>
  </form>
</div>
</template>

<style scoped lang="css">

</style>