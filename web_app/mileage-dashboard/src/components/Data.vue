<template>
  <v-container fluid fill-height>
    <v-layout justify-center>
      <v-flex xs12 sm8 md9>
        <v-card class="elevation-12">
          <table>
            <div v-for="(request, index) in requests" :key="index">
              <tr>
                <th>Date</th>
                <th>Miles</th>
                <th>Kms</th>
              </tr>
              <tr>
                <td>{{ request.date }}</td>
                <td>{{ request.mileage_kms_total }}</td>
                <td>{{ request.mileage_miles_total }}</td>
              </tr>
            </div>
          </table>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
    
</template>

<script>
import axios from 'axios';

export default {
     data: () => ({
       requests: []
  }),
  methods: {
     getRequests() {
          // Get request from the back-end server API.
          //const path = 'http://10.34.44.58:5000/requests';
          const path = 'http://localhost:5000/requests';
          axios.get(path)
            .then((res) => {
              this.requests = res.data.requests;
            })
        }
  },
  created() {
    this.getRequests();
  }
}
</script>