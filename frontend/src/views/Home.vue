<template>
  <div class="home">

  </div>
</template>

<script>
import io from "socket.io-client";

export default {
  name: "Home",
  data() {
    return {
      receivedMessage: null
    }
  },
  created() {
    const socketClient = io.connect("http://localhost:12001");
    console.log(socketClient);
    socketClient.on("connect", () => { 
      console.log("connection server");
       });
  }
};
</script>
