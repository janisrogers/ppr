<template lang="pug">
  div
    v-container(class="view-container")
      article(id="dashboardArticle")
        header
          h1 PPR Sample Home Page

        div(class="page-content")
          div(class="page-content__main")
            section
              header
                h2 Sample home page content

          aside(class="page-content__aside")
            section
              header
                h2 Sample Aside Section

    v-container(v-if="featureOne")
      v-btn(class="form-primary-btn", @click="login", color="primary") Login

    v-container(v-if="featureTwo")
      div Feature two is active
</template>

<script lang="ts">
  import {createComponent, inject, ref} from "@vue/composition-api";
  import {Data} from "@vue/composition-api/dist/ts-api/component";
  import {useRouter} from '@/router/router'

  export default createComponent({
    setup(): Data {
      const router = useRouter()
      const featureOne = inject("featureOne", ref(false))
      const featureTwo = inject("featureTwo", ref(false))

      function login(): void {
        router.push('auth')
      }

      return { featureOne, featureTwo, login }
    }
  })
</script>