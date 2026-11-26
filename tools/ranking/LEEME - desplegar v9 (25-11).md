# Servidor del ranking, v9 (25-11-2026)

**Qué cambia respecto a la v8.** Cuando un alumno sale del ranking, la v8 solo borraba su fila en «Jugadores». En «Juegos» quedaban sus puntos, y en «Cuadrigas fantasmas» su alias, su grupo y sus carreras. La app le promete que «se borrarán del ranking tu alias, tu grupo, tu nombre y tus puntos», de modo que la v9 borra también esas filas. Los resultados de Cuadrigas que van al profesor (pestaña «Cuadrigas») no se tocan, porque son entregas de clase y el juego avisa al alumno de que su profesor los recibe.

**Cómo desplegarla sin cambiar la URL.**
1. Abre el proyecto de Apps Script del ranking y sustituye el contenido de Código.gs por el de «Codigo_v9.js».
2. Guarda y entra en Implementar, después en Gestionar implementaciones. Edita la implementación que ya existe (el lápiz), elige Versión nueva y pulsa Implementar. Si se crea una implementación nueva, la URL cambia y la app deja de funcionar.
3. En el editor, elige la función «limpiarHuerfanos» y pulsa Ejecutar una sola vez. Borra las filas que dejaron las bajas anteriores, y en el registro de ejecución verás cuántas eran.
4. Haz la prueba con un alumno de ensayo, que se da de alta, juega a Arena o a Cuadrigas y sale. Comprueba que no queda nada suyo en «Juegos» ni en «Cuadrigas fantasmas».

**Lo que la v9 no cambia, y conviene que decidas.**
- **El PIN de la clase de repaso.** El 15-11 pediste que fuera dentro de la página, y por eso está en «repaso/profesor.html», en «repaso/pantalla.html» y en este fichero, que se publica en el repositorio público. Con él, cualquiera que lo lea puede abrir rondas o expulsar jugadores, aunque no ve datos personales. La solución es dejar el PIN vacío en las dos páginas, que ya están preparadas para pedirlo una vez y recordarlo en el navegador. En el servidor se leería de las propiedades del script y se cambiaría por uno nuevo.
- **«Cerrar sesión» en la app.** No borra el progreso de Arena (claves harena.*) guardado en el dispositivo.
- **El aviso a los alumnos**, si decides darlo, y la fecha del arreglo para la declaración ética del paper 4.
