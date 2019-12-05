<template>
  <v-app>
    <v-app-bar app>
      <Toolbar></Toolbar>
    </v-app-bar>
    <v-content>
      <Data></Data>
    </v-content>
  </v-app>
</template>

<script>
import Toolbar from './components/Toolbar' 
import Data from './components/Data'

export default {
  name: 'App',
  components: {
    Toolbar,
    Data
  },
  data: () => ({
  }),
};
</script>
