<template>
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <h1 class="abril-fatface-regular text-[46px]">Kassid</h1>
    <BreadCrumbs />

    <!-- todo: convert to hidden file input, codepen might have some ideas on how to detect file hovering -->
    <div class="w-full h-full grid mb-8 place-content-center text-center gap-8">
      <!-- todo: if a file is uploaded (and it fails), this image is replaced with an error container -->
      <img src="/public/assets/fileUploadImage.svg" alt="upload_img" height="200px" class="mx-auto"></img>
      
      <div class="flex flex-col abyssinica-sil-regular text-2xl text-text-normal">
        <h1 class="abyssinica-sil-regular text-[38px] text-text-heading">Lohista ja aseta oma fail siia!</h1>
        <p>Lae üles PDF, DOCX, DOC or XLSX faile</p>
        <p>Faili maksimum suurus on 5 MB</p>
      </div>

      <div class="flex gap-2 justify-center">
        <Button
          class="bg-primary-normal text-text-button abyssinica-sil-regular uppercase text-[14px] w-[200px] min-h-12"
        >
          <HiOutlineUpload size="20"></HiOutlineUpload>
          Lae üles
        </Button>

        <Button
          class="bg-neutral-white text-primary-normal border-primary-normal border-0.5 abyssinica-sil-regular uppercase text-[14px] w-[200px] min-h-12"
        >
          Sisesta manuaalselt
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import Button from '@/components/atoms/Button.vue';
import BreadCrumbs from '@/components/organisms/BreadCrumbs.vue';

import { HiOutlineUpload } from 'vue-icons-plus/hi';
</script>

<style lang="css" scoped>

</style>