from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from qorder.views import orderListJson, suminListJson

from django.contrib.auth.decorators import login_required


from . import views


urlpatterns = [

    url(r'^user/password/$', views.change_password, name='change_password'),
    url(r'^user/about/$', views.about, name='about'),

    # GESTION TERMINALES PORTATILES
    url(r'^qoadmin/tp/gestion/$', views.atp_main, name='atp_main'),
    url(r'^qoadmin/tp/edit_tp/$', views.atp_edit, name='atp_edit'),
    url(r'^qoadmin/tp/edit1_tp/$', views.atp_edit1, name='atp_edit1'),
    url(r'^qoadmin/tp/cflags/$', views.tp_cflags, name='tp_cflags'),

    # SEMANA DE TRABAJO
    url(r'^semana/$', views.semana, name='semana'),
    url(r'^semana_save/$', views.semana_save, name='semana_save'),
    # GESTION TECNICOS
    url(r'^qoadmin/tecnicos/gestion/$', views.tecnicos_main, name='tecnicos_main'),
    url(r'^qoadmin/tecnicos/gt_tabla$', views.gt_tabla, name='gt_tabla'),
    url(r'^qoadmin/tecnicos/save/$', views.tecnico_save, name='tecnico_save'),
    url(r'^qoadmin/tecnicos/new/$', views.tecnico_new, name='tecnico_new'),
    url(r'^qoadmin/tecnicos/edit/$', views.tecnico_edit, name='tecnico_edit'),
    url(r'^qoadmin/tecnicos/cflags/$', views.tecnico_cflag, name='tecnico_cflags'),
    url(r'^qoadmin/tecnicos/tecnico/$',
        views.tecnico_liberarTPL, name='tecnico_liberarTPL'),

    # GESTION ANOMALIAS
    url(r'^qoadmin/anomalias/gestion/$',
        views.anomalias_main, name='anomalias_main'),
    url(r'^qoadmin/anomalias/gt_tabla$',
        views.anomalias_tabla, name='anomalias_tabla'),
    url(r'^qoadmin/anomalias/save/$', views.anomalias_save, name='anomalias_save'),
    url(r'^qoadmin/anomalias/edit/$', views.anomalias_edit, name='anomalias_edit'),
    url(r'^qoadmin/anomalias/new/$', views.anomalias_new, name='anomalias_new'),
    url(r'^qoadmin/anomalias/cflags/$',
        views.anomalias_cflags, name='anomalias_cflags'),
    url(r'^qoadmin/anomalias/anomalias_obs/$',
        views.anomalias_obs, name='anomalias_obs'),
    url(r'^qoadmin/anomalias/agregarobservaciones/$',
        views.agregarobservaciones, name='agregarobservaciones'),



    # GESTION CODIGOS
    url(r'^qoadmin/codigos/gestion/$', views.codigos_main, name='codigos_main'),
    url(r'^qoadmin/codigos/gt_tabla$', views.codigos_tabla, name='codigos_tabla'),
    url(r'^qoadmin/codigos/save/$', views.codigos_save, name='codigos_save'),
    url(r'^qoadmin/codigos/edit/$', views.codigos_edit, name='codigos_edit'),
    url(r'^qoadmin/codigos/new/$', views.codigos_new, name='codigos_new'),
    url(r'^qoadmin/codigos/cflags/$', views.codigos_cflags, name='codigos_cflags'),

    # GESTION ENCUESTAS
    url(r'^qoadmin/encuestas/gestion/$',
        views.encuestas_main, name='encuestas_main'),
    url(r'^qoadmin/encuestas/save/$', views.encuestas_save, name='encuestas_save'),
    url(r'^qoadmin/encuestas/edit/$', views.encuestas_edit, name='encuestas_edit'),
    url(r'^qoadmin/encuestas/new/$', views.encuestas_new, name='encuestas_new'),
    url(r'^qoadmin/encuestas/cflags/$',
        views.encuestas_cflags, name='encuestas_cflags'),
    url(r'^qoadmin/encuestas/detail/$',
        views.encuesta_detail, name='encuesta_detail'),
    url(r'^qoadmin/encuestas/newpregunta/$',
        views.pregunta_new, name='pregunta_new'),
    url(r'^qoadmin/encuestas/savepregunta/$',
        views.pregunta_save, name='pregunta_save'),
    url(r'^qoadmin/encuestas/editpregunta/$',
        views.pregunta_edit, name='pregunta_edit'),
    url(r'^qoadmin/encuestas/ordenpregunta/$',
        views.pregunta_orden, name='pregunta_orden'),
    # GESTION PROBLEMAS
    url(r'^qoadmin/problemas/gestion/$',
        views.problemas_main, name='problemas_main'),
    url(r'^qoadmin/problemas/gt_tabla$',
        views.problemas_tabla, name='problemas_tabla'),
    url(r'^qoadmin/problemas/save/$', views.problemas_save, name='problemas_save'),
    url(r'^qoadmin/problemas/edit/$', views.problemas_edit, name='problemas_edit'),
    url(r'^qoadmin/problemas/new/$', views.problemas_new, name='problemas_new'),
    url(r'^qoadmin/problemas/cflags/$',
        views.problemas_cflags, name='problemas_cflags'),


    # GESTION TIPOS ORDENES
    url(r'^qoadmin/tiposordenes/gestion/$',
        views.tiposordenes_main, name='tiposordenes_main'),
    url(r'^qoadmin/tiposordenes/gt_tabla$',
        views.tiposordenes_tabla, name='tiposordenes_tabla'),
    url(r'^qoadmin/tiposordenes/propiedades$',
        views.tiposordenes_propiedades, name='tiposordenes_propiedades'),
    url(r'^qoadmin/tiposordenes/anomaliaxtipo_save$',
        views.tiposordenes_anomaliaxtipo_save, name='tiposordenes_anomaliaxtipo_save'),
    url(r'^qoadmin/tiposordenes/anomaliaxtipo_cflags$',
        views.anomaliaxtipo_cflags, name='anomaliaxtipo_cflags'),

    # GESTION RUTA_SUM
    url(r'^qoadmin/rutasum/gestion/$', views.rutasum_main, name='rutasum_main'),
    url(r'^qoadmin/rutasum/rutasum_tabla$',
        views.rutasum_tabla, name='rutasum_tabla'),
    url(r'^qoadmin/rutasum/rutasum_edit$',
        views.rutasum_edit, name='rutasum_edit'),
    url(r'^qoadmin/rutasum/rutasum_new$', views.rutasum_new, name='rutasum_new'),
    url(r'^qoadmin/rutasum/rutasum_save$',
        views.rutasum_save, name='rutasum_save'),
    url(r'^qoadmin/rutasum/suministro_tabla$',
        views.suministro_tabla, name='suministro_tabla'),
    url(r'^qoadmin/rutasum/tabla_suministros_sin_ruta$',
        views.tabla_suministros_sin_ruta, name='tabla_suministros_sin_ruta'),
    url(r'^qoadmin/rutasum/trasferir_suministro$',
        views.trasferir_suministro, name='trasferir_suministro'),
    url(r'^qoadmin/rutasum/rutasum_delete$',
        views.rutasum_delete, name='rutasum_delete'),
    url(r'^qoadmin/rutasum/suministro_delete$',
        views.suministro_delete, name='suministro_delete'),

    # GENERACION
    url(r'^qoordenes/generacion/main/$',
        views.generacion_main, name='generacion_main'),
    url(r'^qoordenes/generacion/generacion_ruta/$',
        views.generacion_ruta, name='generacion_ruta'),
    url(r'^qoordenes/generacion/generar/$', views.generar, name='generar'),



    # ASIGNACION
    url(r'^qoordenes/asignacion/main/$',
        views.asignacion_main, name='asignacion_main'),
    url(r'^qoordenes/asignacion/attable/$',
        views.asignacion_tech, name='asignacion_tech'),
    url(r'^qoordenes/asignacion/artable/$',
        views.asignacion_route, name='asignacion_route'),
    url(r'^qoordenes/asignacion/asignar_route/$',
        views.asignar_route, name='asignar_route'),
    url(r'^qoordenes/asignacion/asignar_asign/$',
        views.asignacion_asignaciones, name='asignacion_asignaciones'),
    url(r'^qoordenes/asignacion/asignar_desasign/$',
        views.asignacion_desasignar, name='asignacion_desasignar'),
    url(r'^qoordenes/asignacion/guardar_asignar_ordenes/$',
        views.guardar_asignar_ordenes, name='guardar_asignar_ordenes'),
    


    # SEGMENTACIÓN RUTAS
     url(r'^qoordenes/segmentacion_rutas/main/$',
        views.segmentacion_rutas_main, name='segmentacion_rutas_main'),
     url(r'^qoordenes/segmentacion_rutas/obtener_rutas_segmentos/$',
        views.obtener_rutas_segmentos, name='obtener_rutas_segmentos'),
     url(r'^qoordenes/asignacion/segmento/artable/$',
        views.asignacion_segmento_route, name='asignacion_segmento_route'),
     url(r'^qoordenes/segmentacion_rutas/coordenadas/$',
        views.segmentacion_rutas_coordenadas, name='segmentacion_rutas_coordenadas'),
     url(r'^qoordenes/segmentacion/save/$',
        views.segmentacion_save, name='segmentacion_save'),
    url(r'^qoordenes/segmentacion/asignacion/save/$',
        views.segmentacion_asignacion_save, name='segmentacion_asignacion_save'),
    url(r'^qoordenes/segmentacion/asignacion/update/$',
        views.segmentacion_asignacion_update, name='segmentacion_asignacion_update'),
    url(r'^qoordenes/segmentacion/segmentos/show/$',
        views.segmentacion_segmentos_show, name='segmentacion_segmentos_show'),
    url(r'^qoordenes/segmentacion/segmentos/edit/$',
        views.segmentacion_segmentos_edit, name='segmentacion_segmentos_edit'),
    url(r'^qoordenes/segmentacion/segmentos/delete/$',
        views.segmentacion_segmentos_delete, name='segmentacion_segmentos_delete'),
    url(r'^qoordenes/segmentacion/segmentos/update/$',
        views.segmentacion_segmentos_update, name='segmentacion_segmentos_update'),
    url(r'^qoordenes/segmentacion/areas/update/$',
        views.segmentacion_areas_show, name='segmentacion_areas_show'),
    url(r'^qoordenes/asignacion/segmento/area/delete$',
        views.asignacion_segmento_area_delete, name='asignacion_segmento_area_delete'),
    # SEGMENTACION PUNTOS DE SUMINISTROS SIN COORDENADAS
    url(r'^qoordenes/asignacion/table/puntos_sincoord/$',
        views.asignacion_table_puntos_sincoord, name='asignacion_table_puntos_sincoord'),
    url(r'^qoordenes/asignacion/ubicacion/save/$',
        views.asignacion_ubicacion_save, name='asignacion_ubicacion_save'),
   
    #ASIGNACION DE LA SEGMENTACIÓN
   url(r'^qoordenes/asignacion/attable/seg/$',
        views.asignacion_tech_seg, name='asignacion_tech_seg'),
   url(r'^qoordenes/asignacion/segmento/table$',
        views.asignacion_segmento_table, name='asignacion_segmento_table'), 
    url(r'^qoordenes/asignacion/asignaciones/seg/table$',
        views.asignacion_asignaciones_seg, name='asignacion_asignaciones_seg'),
    url(r'^qoordenes/asignacion/asignar_segmento/$',
        views.asignar_segmento, name='asignar_segmento'),
    url(r'^qoordenes/asignacion/desasignar_segmento/$',
        views.asignacion_desasignar_segmento, name='asignacion_desasignar_segmento'),
    url(r'^qoordenes/asignacion/guardar_asignar_segmentos/$',
        views.guardar_asignar_segmentos, name='guardar_asignar_segmentos'),
    
    # DIVISION
    url(r'^qoordenes/division/$', views.dividir, name='dividir'),
    url(r'^qoordenes/generardivision/$',
        views.generardivision, name='generar_division'),
    url(r'^qoordenes/quitardivision/$',
        views.quitardivision, name='quitardivision'),
    url(r'^qoordenes/division/drtable/$',
        views.division_route, name='division_route'),
    url(r'^qoordenes/division/ddtable/$',
        views.list_divisiones, name='lista_divisiones'),
    url(r'^qoordenes/division/dstable/$',
        views.list_suministros_ruta, name='lista_suministros_ruta'),
    url(r'^qoordenes/division/dsdtable/$', views.list_suministros_division,
        name='lista_suministros_division'),
    url(r'^qoordenes/division/moverordenes/$',
        views.mover_ordenes, name='moverordenes'),
    #url(r'^qoadmin/tiposordenes/gt_tabla$', views.tiposordenes_tabla, name='tiposordenes_tabla'),
    #url(r'^qoadmin/tiposordenes/propiedades$', views.tiposordenes_propiedades, name='tiposordenes_propiedades'),
    #url(r'^qoadmin/tiposordenes/anomaliaxtipo_save$', views.tiposordenes_anomaliaxtipo_save, name='tiposordenes_anomaliaxtipo_save'),

    # MONITOR
    url(r'^qoordenes/monitor/main/$', views.monitor_main, name='monitor_main'),
    url(r'^qoordenes/monitor/attable/$', views.monitor_tech, name='monitor_tech'),
    url(r'^qoordenes/monitor/estado/$',
        views.monitor_estado, name='monitor_estado'),
    url(r'^qoordenes/monitor/monitor_getorders/$',
        views.monitor_getorders, name='monitor_getorders'),
    url(r'^my/datatable/data/$', orderListJson.as_view(), name='order_list_json'),
    url(r'^qoordenes/monitor/monitor_getorder/$',
        views.monitor_getorder, name='monitor_getorder'),

    # MONITOR_RUTAS
    url(r'^qoordenes/monitor_rutas/main/$',
        views.monitor_rutas_main, name='monitor_rutas_main'),
    url(r'^qoordenes/monitor_rutas/attable/$',
        views.monitor_rutas, name='monitor_rutas'),
    url(r'^qoordenes/monitor_rutas/estado/$',
        views.monitor_rutas_estado, name='monitor_rutas_estado'),
    url(r'^qoordenes/monitor_rutas/monitor_getorders/$',
        views.monitor_getorders, name='monitor_rutas_getorders'),
    url(r'^my/datatable/data/$', orderListJson.as_view(), name='order_list_json'),
    url(r'^qoordenes/monitor_rutas/monitor_getorder/$',
        views.monitor_getorder, name='monitor_rutas_getorder'),

    # CONSULTA
    url(r'^qoordenes/consulta/main/$', views.consulta_main, name='consulta_main'),
    url(r'^qoordenes/consulta/crtable/$',
        views.consulta_route, name='consulta_route'),
    url(r'^qoordenes/consulta/listasum/$',
        views.lista_suministros, name='lista_suministros'),
    url(r'^qoordenes/consulta/data/$',
        suminListJson.as_view(), name='sum_list_json'),
    url(r'^qoordenes/consulta/datosum/$',
        views.datos_suministro, name='datos_suministro'),
    url(r'^qoordenes/consulta/estado_ruta/$',
        views.estado_ruta, name='estado_ruta'),

    # REVISION
    url(r'^qoordenes/revision/main/$', views.revision_main, name='revision_main'),
    url(r'^qoordenes/revision/confirmar_lectura/$',
        views.confirmar_lectura, name='confirmar_lectura'),
    url(r'^qoordenes/revision/corregir_lectura/$',
        views.corregir_lectura, name='corregir_lectura'),
    url(r'^qoordenes/revision/get_desc_anom/$',
        views.get_desc_anom, name='get_desc_anom'),
    url(r'^qoordenes/revision/deleteanom/$',
        views.deleteanom, name='deleteanom'),
    url(r'^qoordenes/revision/updateanom/$',
        views.updateanom, name='updateanom'),
    url(r'^qoordenes/revision/addanomalia/$',
        views.addanomalia, name='addanomalia'),


    # CLIENTE
    url(r'^qoadmin/clientes/main/$', views.clientes_main, name='clientes_main'),
    url(r'^qoadmin/clientes/buscar/$',
        views.buscar_cliente, name='buscar_cliente'),
    url(r'^qoadmin/clientes/save/$', views.cliente_save, name='cliente_save'),
    url(r'^qoadmin/contactos/edit/$', views.contacto_edit, name='contacto_edit'),
    url(r'^qoadmin/contactos/new/$', views.contacto_new, name='contacto_new'),
    url(r'^qoadmin/contactos/save/$', views.contacto_save, name='contacto_save'),
    url(r'^qoadmin/contactos/delete/$',
        views.contacto_delete, name='contacto_delete'),



    # FORZADO
    url(r'^qoordenes/forzado/main/$', views.forzado_main, name='forzado_main'),
    url(r'^qoordenes/forzado/forzar_ruta_no_leida/$',
        views.forzar_ruta_no_leida, name='forzar_ruta_no_leida'),
    url(r'^qoordenes/forzado/forzar_ruta_leida/$',
        views.forzar_ruta_leida, name='forzar_ruta_leida'),
    url(r'^qoordenes/forzado/forzar_rutas/$',
        views.forzar_rutas, name='forzar_rutas'),


    # GEOFENCING
    url(r'^qoordenes/geofencing/main/$',
        views.geofencing_main, name='geofencing_main'),
    url(r'^qoordenes/geofencing/list/$',
        views.geofencing_list, name='geofencing_list'),
    url(r'^qoordenes/geofencing/new/$',
        views.geofencing_new, name='geofencing_new'),
    url(r'^qoordenes/geofencing/edit/$',
        views.geofencing_edit, name='geofencing_edit'),
    url(r'^qoordenes/geofencing/save/$',
        views.geofencing_save, name='geofencing_save'),
    url(r'^qoordenes/geofencing/detail/$',
        views.geofencing_detail, name='geofencing_detail'),
    url(r'^qoordenes/geofencing/savedetail/$',
        views.geofencing_savedetail, name='geofencing_savedetail'),
    url(r'^qoordenes/geofencing/geofencing_cflags/$',
        views.geofencing_cflags, name='geofencing_cflags'),



    # IMPORTACION
    url(r'^qointerfaz/importacion/$', views.importacion, name='importacion'),
    url(r'^qointerfaz/make_import/$', views.make_import, name='make_import'),
    url(r'^qointerfaz/obtener_avance/$',
        views.obtener_avance, name='obtener_avance'),
    url(r'^qointerfaz/log_import/$', views.log_import, name='log_import'),
    url(r'^qointerfaz/Savefiles/$', views.Savefiles, name='Savefiles'),
    url(r'^qointerfaz/delete_files/$', views.delete_files, name='delete_files'),
    url(r'^qointerfaz/mostrar_archivos/$',
        views.mostrar_archivos, name='mostrar_archivos'),


    # EXPORTACION
    url(r'^qointerfaz/exportacion/$', views.exportacion, name='exportacion'),
    url(r'^qointerfaz/make_export/$', views.make_export, name='make_export'),
    url(r'^qointerfaz/result_exportacion/$',
        views.result_exportacion, name='result_exportacion'),
    url(r'^qoadminnterfaz/tables_routes/$',
        views.tables_routes, name='tables_routes'),
    url(r'^qoadminnterfaz/archivo_exportacion/$',
        views.archivo_exportacion, name='archivo_exportacion'),
    url(r'^qoadminnterfaz/send_file/$', views.send_file, name='send_file'),



    # REORGANIZACION
    url(r'^qoordenes/reorganizacion/main$',
        views.reorganizacion_main, name='reorganizacion_main'),
    url(r'^qoordenes/reorganizacion/reorganizacion_list$',
        views.reorganizacion_list, name='reorganizacion_list'),
    url(r'^qoordenes/reorganizacion/autorizar$',
        views.autorizar, name='autorizar'),
    url(r'^qoordenes/reorganizacion/denegar$', views.denegar, name='denegar'),
    url(r'^qoordenes/reorganizacion/posicionmapa$',
        views.posicionmapa, name='posicionmapa'),
    url(r'^qoordenes/reorganizacion/export_reorganizar$',
        views.export_reorganizar, name='export_reorganizar'),



    # MAPAS LP
    url(r'^maps/ultima_posicion$', views.ultima_posicion, name='ultima_posicion'),
    url(r'^maps/maps_up_techs$', views.maps_up_techs, name='maps_up_techs'),
    url(r'^maps/up_map$', views.get_map_last_p, name='get_map_last_p'),
    # MAPAS RECORRIDO
    url(r'^maps/recorrido$', views.recorrido, name='recorrido'),
    url(r'^maps/maps_route_techs$', views.maps_route_techs, name='maps_route_techs'),
    url(r'^maps/get_map_route$', views.get_map_route, name='get_map_route'),
    url(r'^maps/get_data_activity$',
        views.get_data_activity, name='get_data_activity'),

    # LISTADO RECORRIDO
    url(r'^maps/listadorecorrido$', views.listadorecorrido, name='listadorecorrido'),
    url(r'^maps/listadorecorrido_techs$',
        views.listadorecorrido_techs, name='listadorecorrido_techs'),
    url(r'^maps/get_listadorecorrido$',
        views.get_listadorecorrido, name='get_listadorecorrido'),


    # CONFIGURACION
    url(r'^qosettings/configuracion/$', views.configuracion, name='configuracion'),
    url(r'^qosettings/configuracion/edit/$',
        views.configuracion_edit, name='configuracion_edit'),
    url(r'^qosettings/configuracion/new/$',
        views.configuracion_new, name='configuracion_new'),
    url(r'^qosettings/configuracion/save/$',
        views.configuracion_save, name='configuracion_save'),
    url(r'^qosettings/configuracion/delete/$',
        views.configuracion_delete, name='configuracion_delete'),


    # SOPORTE PUSH

    url(r'^qosoporte/push/$', views.soporte_main, name='soporte_main'),
    url(r'^qosoporte/push/soporte_get_terminales$', views.soporte_get_terminales, name='soporte_get_terminales'),
    url(r'^qosoporte/push/ejecutar_soporte$', views.ejecutar_soporte, name='ejecutar_soporte'),
    url(r'^qosoporte/push/get_soporte$', views.get_soporte, name='get_soporte'),

    #GENERICAS
    url(r'^generic/download_file', views.download_file, name='get_download_link'),  
        

    # REPORTES
    url(r'^qoreportes/anomalia/$', views.reporte_anomalia, name='reporte_anomalia'),
    url(r'^qoreportes/anomalia_ruta/$', views.table_routes, name='table_routes'),
    url(r'^qoreportes/anomalia_reporte/$',
        views.get_listadoanomalia, name='get_listadoanomalia'),

    url(r'^qoreportes/rpt_anomalias_ruta/$',
        views.rpt_anomalias_rutas, name='rpt_anomalias_rutas'),
    url(r'^qoreportes/rpt_anomalias_ruta/rutas_sum/$',
        views.rpt_anomalias_rutas_getrutassum, name='rpt_anomalias_rutas_getrutassum'),
    url(r'^qoreportes/rpt_anomalias_ruta/resul/$',
        views.rpt_anomalias_rutas_getreporte, name='rpt_anomalias_rutas_getreporte'),


    url(r'^qoreportes/rpt_lecturas_ruta/$',
        views.rpt_lecturas_rutas, name='rpt_lecturas_rutas'),
    url(r'^qoreportes/rpt_lecturas_ruta/rutas_sum/$',
        views.rpt_lecturas_rutas_getrutassum, name='rpt_lecturas_rutas_getrutassum'),
    url(r'^qoreportes/rpt_lecturas_ruta/resul/$',
        views.rpt_lecturas_rutas_getreporte, name='rpt_lecturas_rutas_getreporte'),


    url(r'^qoreportes/rpt_sum_alta_modif/$',
        views.rpt_sum_alta_modif, name='rpt_sum_alta_modif'),
    url(r'^qoreportes/rpt_sum_alta_modif/rutas_sum/$',
        views.rpt_sum_alta_modif_getrutassum, name='rpt_sum_alta_modif_getrutassum'),
    url(r'^qoreportes/rpt_sum_alta_modif/resul/$',
        views.rpt_sum_alta_modif_getreporte, name='rpt_sum_alta_modif_getreporte'),


    url(r'^qoreportes/reporte_fh/$', views.reporte_fh, name='reporte_fh'),
    url(r'^qoreportes/rpt_hora_rutas_getrutassum/$',
        views.rpt_hora_rutas_getrutassum, name='rpt_hora_rutas_getrutassum'),
    url(r'^qoreportes/rpt_hora_rutas_getreporte/$',
        views.rpt_hora_rutas_getreporte, name='rpt_hora_rutas_getreporte'),
    url(r'^qoreportes/obtener_lecturistas/$',
        views.obtener_lecturistas, name='obtener_lecturistas'),


    url(r'^qoreportes/reporte_consumo/$',
        views.reporte_consumo, name='reporte_consumo'),
    url(r'^qoreportes/rpt_consumo_rutas_getrutassum/$',
        views.rpt_consumo_rutas_getrutassum, name='rpt_consumo_rutas_getrutassum'),
    url(r'^qoreportes/rpt_consumo_rutas_getreporte/$',
        views.rpt_consumo_rutas_getreporte, name='rpt_consumo_rutas_getreporte'),

    url(r'^qoreportes/rpt_exportacion_rutas/$',
        views.rpt_exportacion_rutas, name='rpt_exportacion_rutas'),
    url(r'^qoreportes/rpt_exportadas_rutas_getreporte/$',
        views.rpt_exportadas_rutas_getreporte, name='rpt_exportadas_rutas_getreporte'),



    url(r'^qoreportes/reporte_desemp_lect/$',
        views.reporte_desemp_lect, name='reporte_desemp_lect'),
    url(r'^qoreportes/obtener_desemp_lect/$',
        views.obtener_desemp_lect, name='obtener_desemp_lect'),
    url(r'^qoreportes/rpt_desemp_rutas_getrutassum/$',
        views.rpt_desemp_rutas_getrutassum, name='rpt_desemp_rutas_getrutassum'),
    url(r'^qoreportes/rpt_desemp_lect_getreporte/$',
        views.rpt_desemp_lect_getreporte, name='rpt_desemp_lect_getreporte'),



    # Consulta orden detallada
    url(r'^qoordenes/consulta/datalle/$',
        views.consulta_orden_detallada, name='consulta_orden_detallada'),


    # Reorganización GU
    url(r'^qoordenes/reorganizacion_gu/main/$',
        views.reorganizcion_gu_main, name='reorganizcion_gu_main'),
    url(r'^qoordenes/reorganizacion_gu/cargar_suministros/$',
        views.cargar_suministros, name='cargar_suministros'),
    url(r'^qoordenes/reorganizacion_gu/insertar_suministro/$',
        views.insertar_suministro, name='insertar_suministro'),
    url(r'^qoordenes/reorganizacion_gu/obtener_rutas/$',
        views.obtener_rutas, name='obtener_rutas'),
    url(r'^qoordenes/reorganizacion_gu/reinsertar_suministro/$',
        views.reinsertar_suministro, name='reinsertar_suministro'),

    # GESTION PARAMETROS CLIENTES
    url(r'^qoadmin/config_acciones_clientes/config_acciones_cliente_main/$',
        views.config_acciones_cliente_main, name='config_acciones_cliente_main'),
    url(r'^qoadmin/config_acciones_clientes/obtener_configuraciones/$',
        views.get_configuraciones, name='get_configuraciones'),
    url(r'^qoadmin/config_acciones_clientes/nueva_configuracion/$',
        views.nueva_configuracion, name='nueva_configuracion'),
    url(r'^qoadmin/config_acciones_clientes/getconfiguracion_edit/$',
        views.getconfiguracion_edit, name='getconfiguracion_edit'),
    url(r'^qoadmin/config_acciones_clientes/editar_configuracion/$',
        views.editar_configuracion, name='editar_configuracion'),
    url(r'^qoadmin/config_acciones_clientes/delete_configuracion/$',
        views.delete_configuracion, name='delete_configuracion'),
    url(r'^qoadmin/config_acciones_clientes/asig_accion_config/$',
        views.asig_accion_config, name='asig_accion_config'),
    url(r'^qoadmin/config_acciones_clientes/cargar_acciones_config/$',
        views.cargar_acciones_config, name='cargar_acciones_config'),
    url(r'^qoadmin/config_acciones_clientes/get_clientes_config/$',
        views.get_clientes_config, name='get_clientes_config'),
    url(r'^qoadmin/config_acciones_clientes/get_clientes_filtro/$',
        views.get_clientes_filtro, name='get_clientes_filtro'),
    url(r'^qoadmin/config_acciones_clientes/asignar_clientes_config/$',
        views.asignar_clientes_config, name='asignar_clientes_config'),
    url(r'^qoadmin/config_acciones_clientes/delete_cli_indiv_config/$',
        views.delete_cli_indiv_config, name='delete_cli_indiv_config'),
    url(r'^qoadmin/config_acciones_clientes/delete_accion_config/$',
        views.delete_accion_config, name='delete_accion_config'),
    url(r'^qoadmin/config_acciones_clientes/del_all_cfg/$',
        views.del_all_cfg, name='del_all_cfg'),
    url(r'^qoadmin/config_acciones_clientes/get_rutas_per_oficina/$',
        views.get_rutas_per_oficina, name='get_rutas_per_oficina'),
    url(r'^qoadmin/config_acciones_clientes/asign_config_bulk/$',
        views.asign_config_bulk, name='asign_config_bulk'),
    url(r'^qoadmin/config_acciones_clientes/asign_cliente_aleatorio/$',
        views.asign_cliente_aleatorio, name='asign_cliente_aleatorio'),
    url(r'^qoadmin/config_acciones_clientes/del_allclientes_cfg/$',
        views.del_allclientes_cfg, name='del_allclientes_cfg'),
    url(r'^qoadmin/config_acciones_clientes/asign_masivo_clien_aleatorio/$',
        views.asign_masivo_clien_aleatorio, name='asign_masivo_clien_aleatorio'),


    # REPORTE DE AUDITORIA DE LECTURA----ACCION CONFIGS CLIENTE---
    url(r'^qoreportes/reporte_auditoria_lect/reporte_auditoria_lect/$',
        views.reporte_auditoria_lect, name='reporte_auditoria_lect'),
    url(r'^qoreportes/reporte_auditoria_lect/reporte_auditoria_lect_getreporte/$',
        views.reporte_auditoria_lect_getreporte, name='reporte_auditoria_lect_getreporte'),
    url(r'^qoreportes/reporte_auditoria_lect/get_tecnicos_from_oficina/$',
        views.get_tecnicos_from_oficina, name='get_tecnicos_from_oficina'),
    url(r'^qoreportes/reporte_auditoria_lect/consulta_foto/$',
        views.consulta_foto, name='consulta_foto'),

]
