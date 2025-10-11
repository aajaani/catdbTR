<script setup lang="ts">

import BreadCrumbs from "@/components/organisms/BreadCrumbs.vue";
import FilterTable from "@/components/organisms/FilterTable.vue";

import { MdArrowOutward } from "vue-icons-plus/md";
import { FiEdit3 } from "vue-icons-plus/fi";
import { HiOutlineTrash } from "vue-icons-plus/hi";

import { defineTable, field, type RowEntry } from "@/components/FilterTable";

import TableText from "@/components/atoms/filter-table/Text.vue"
import TableStatus from "@/components/atoms/filter-table/Status.vue"

import Actions from "@/components/molecules/filter-table/Actions.vue";

type CatStatus = "looking-for-home" | "in-new-home" | "reserved" | "lost" | ":(";
interface Cat {
  id: number,
  name: string,
  status: CatStatus,
  manager_name: string,
  original_colony: string,
  details: string,
  on_homepage: boolean
}
const status_to_color: { [ key in CatStatus ]: "green" | "yellow" | "red" | "black" | "gray" } = {
  "looking-for-home": "yellow",
  "in-new-home": "green",
  ":(": "black",
  "lost": "red",
  "reserved": "gray"
}

const status_to_readable: { [ key in CatStatus ]: string } = {
  "looking-for-home": "Otsib kodu",
  "in-new-home": "Uues kodus",
  ":(": "Kiisudemaal",
  "lost": "Kadunud",
  "reserved": "Broneeritud"
} 

const createMockCat = ( id: number, name: string, status: CatStatus, manager_name: string, original_colony: string, details: string, on_homepage: boolean ): Cat => {
  return {
    id, name, status, manager_name, original_colony, details, on_homepage
  }
}

const mock_cats: Cat[ ] = [
  // gpt generated mock data
  createMockCat(1, "Milo", "looking-for-home", "Sarah Bennett", "Riverside Colony", "Gentle young male, neutered, enjoys sunbathing and chasing feathers.", true),
  createMockCat(2, "Luna", "in-new-home", "Tom Richardson", "Elm Street Colony", "Playful female kitten, loves climbing curtains.", false),
  createMockCat(3, "Oliver", "reserved", "Clara Wu", "Seaside Colony", "Calm and affectionate, good with other cats.", true),
  createMockCat(4, "Leo", "lost", "Jack Dempsey", "Old Mill Colony", "Went missing two weeks ago, last seen near the park.", false),
  createMockCat(5, "Bella", ":(", "Alicia Ford", "Hilltop Colony", "Sickly kitten under treatment for respiratory infection.", false),
  createMockCat(6, "Charlie", "looking-for-home", "Nina Patel", "Maple Grove Colony", "Sociable tomcat, enjoys people and attention.", true),
  createMockCat(7, "Chloe", "reserved", "George Silva", "Pinewood Colony", "Sweet natured, shy at first but warms up quickly.", false),
  createMockCat(8, "Simba", "in-new-home", "Helen Brooks", "Garden Lane Colony", "Now adopted, adjusting well to new family.", false),
  createMockCat(9, "Lucy", "lost", "Mark Green", "Harbor Colony", "Microchipped female, reward offered for return.", false),
  createMockCat(10, "Max", "looking-for-home", "Rachel Yang", "Cedar Grove Colony", "Energetic young cat, loves laser toys.", true),
  createMockCat(11, "Daisy", "looking-for-home", "Patrick O'Neil", "Riverside Colony", "Very gentle with children, purrs constantly.", true),
  createMockCat(12, "Toby", ":(", "Sophia Turner", "Elm Street Colony", "Senior cat recovering from injury, needs calm home.", false),
  createMockCat(13, "Cleo", "reserved", "Mason Kim", "Seaside Colony", "Loves company of other cats, medium-haired beauty.", false),
  createMockCat(14, "Nala", "in-new-home", "Charlotte Lewis", "Old Mill Colony", "Adopted last week, thriving in her new home.", false),
  createMockCat(15, "Misty", "lost", "Daniel Scott", "Hilltop Colony", "White cat with one blue eye, last seen near forest road.", false),
  createMockCat(16, "Oscar", "looking-for-home", "Emma Johnson", "Maple Grove Colony", "Curious and vocal, great companion cat.", true),
  createMockCat(17, "Willow", "reserved", "James Brown", "Pinewood Colony", "Calm and gentle, ideal for quiet households.", false),
  createMockCat(18, "Smokey", "looking-for-home", "Lara Singh", "Garden Lane Colony", "Older male, loves naps and head scratches.", true),
  createMockCat(19, "Loki", ":(", "Oliver Hart", "Harbor Colony", "Undergoing treatment for minor skin condition.", false),
  createMockCat(20, "Mabel", "in-new-home", "Grace Reed", "Cedar Grove Colony", "Adopted by a family with kids; doing very well.", false),
  createMockCat(21, "Pumpkin", "looking-for-home", "Tom Richardson", "Riverside Colony", "Orange tabby with big personality, very playful.", true),
  createMockCat(22, "Mochi", "reserved", "Sarah Bennett", "Elm Street Colony", "Gentle cat that bonds quickly with people.", false),
  createMockCat(23, "Finn", "in-new-home", "Alicia Ford", "Seaside Colony", "Happy in a large rural home with other cats.", false),
  createMockCat(24, "Socks", "lost", "Jack Dempsey", "Old Mill Colony", "Black-and-white cat with unique markings.", false),
  createMockCat(25, "Hazel", ":(", "Helen Brooks", "Hilltop Colony", "Recovering from eye infection, doing better daily.", false),
  createMockCat(26, "Ruby", "looking-for-home", "Clara Wu", "Maple Grove Colony", "Loves attention, perfect lap cat.", true),
  createMockCat(27, "Archie", "reserved", "Mark Green", "Pinewood Colony", "Good temperament, fine with dogs.", false),
  createMockCat(28, "Pearl", "looking-for-home", "Lara Singh", "Garden Lane Colony", "Soft-spoken and affectionate.", true),
  createMockCat(29, "Zeus", "in-new-home", "Nina Patel", "Harbor Colony", "Strong and playful male cat, thriving indoors.", false),
  createMockCat(30, "Minnie", "lost", "George Silva", "Cedar Grove Colony", "Wearing a pink collar with bell.", false),
  createMockCat(31, "Hazel", "looking-for-home", "Patrick O'Neil", "Riverside Colony", "Enjoys cuddles, quiet and kind.", true),
  createMockCat(32, "Milo Jr.", "reserved", "Charlotte Lewis", "Elm Street Colony", "Tiny kitten, reserved by local family.", false),
  createMockCat(33, "Whiskers", "looking-for-home", "Emma Johnson", "Seaside Colony", "Curious explorer, loves outdoor time.", true),
  createMockCat(34, "Zara", ":(", "Mason Kim", "Old Mill Colony", "Feral background, slowly socializing with humans.", false),
  createMockCat(35, "Pepper", "in-new-home", "Grace Reed", "Hilltop Colony", "Recently adopted, very attached to new owner.", false),
  createMockCat(36, "Cinnamon", "looking-for-home", "Lara Singh", "Maple Grove Colony", "Beautiful tortoiseshell with calm demeanor.", true),
  createMockCat(37, "Felix", "reserved", "James Brown", "Pinewood Colony", "Loves treats and gentle brushing.", false),
  createMockCat(38, "Snowball", "lost", "Oliver Hart", "Garden Lane Colony", "Pure white cat, likely hiding nearby.", false),
  createMockCat(39, "Raven", ":(", "Sarah Bennett", "Harbor Colony", "Older cat under hospice care, very gentle.", false),
  createMockCat(40, "Mocha", "looking-for-home", "Tom Richardson", "Cedar Grove Colony", "Playful and affectionate, great with families.", true),
]

const { fields, entries } = defineTable({
    "cat-id": field({
      title: "#",
      component: TableText,
      sortFn: ( p1, p2 ) => {
        return 0;
      }
    }),
    "cat-name": field({
      title: "Kassi nimi",
      component: TableText,
    }),
    "cat-status": ({
      title: "Staatus",
      component: TableStatus,
      fitContent: true
    }),
    "cat-manager-name": field({
      title: "Hooldaja nimi",
      component: TableText,
      fitContent: true
    }),
    "cat-colony": field({
      title: "Originaalne koloonia",
      component: TableText,
    }),
    "cat-details": field({
      title: "Teated",
      component: TableText,
    }),
    "cat-on-homepage": field({
      title: "Kodukal",
      component: TableStatus,
    }),
    "cat-actions": field({
      title: "Tegevused",
      component: Actions
    })
  },
  // uhm linter is very unhappy
  // todo: rework table component structure
  mock_cats.map( ( cat: Cat ) => ({
    "cat-id": {
      text: cat.id.toString( )
    },
    "cat-name": {
      text: cat.name
    },
    "cat-status": {
      color: status_to_color[ cat.status ],
      label: status_to_readable[ cat.status ],
    },
    "cat-manager-name": {
      text: cat.manager_name,
    },
    "cat-colony": {
      text: cat.original_colony
    },
    "cat-details": {
      text: cat.details
    },
    "cat-on-homepage": {
      color: cat.on_homepage ? "green" : "red"
    },
    "cat-actions": {
      actions: [{
        icon: MdArrowOutward,
        onClick: ( ) => { }
      }, {
        icon: FiEdit3,
        onClick: ( ) => { }
      }, {
        icon: HiOutlineTrash,
        onClick: ( ) => { }
      }]
    }
  }))
);
</script>

<template>
  <div class="flex flex-col bg-main-bg px-8 pt-4">
    <!-- todo: kinda overlaps with collapse/back button -->
    <h1 class="abril-fatface-regular text-[46px]">Kassid</h1>
    <BreadCrumbs />

    <FilterTable
      :fields="fields"
      :entries="entries"
    />
  </div>
</template>

<style scoped>

</style>