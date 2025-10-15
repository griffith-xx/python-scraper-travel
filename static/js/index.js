const { createApp, ref } = Vue

createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const message = ref('Hello vue!')
        return {
            message
        }
    }
}).mount('#app')