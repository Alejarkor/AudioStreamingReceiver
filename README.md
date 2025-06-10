# AudioStreamingReceiver

Este proyecto incluye un receptor de streaming optimizado para latencia mínima.
Utiliza GStreamer para reproducir video y audio estéreo en tiempo real.

## Uso

```bash
./stream_receiver.py rtsp://servidor/ruta
```

La tubería de GStreamer se configura con `latency=0` y colas en modo
`leaky` para reducir el retardo. El audio se fuerza a dos canales para
asegurar la reproducción en estéreo.
