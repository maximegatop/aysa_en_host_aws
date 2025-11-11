def CargaBD():
    _sSchemma ="""CREATE TABLE [APACONEN] ( 
    [NUM_OS] [VARCHAR ](8) NOT NULL ON CONFLICT IGNORE, 
    [CO_MARCA] [VARCHAR ](5) NOT NULL ON CONFLICT IGNORE, 
    [NUM_APA] [VARCHAR ](20) NOT NULL ON CONFLICT IGNORE, 
    [TIP_CSMO] [VARCHAR ](5) NOT NULL ON CONFLICT IGNORE, 
    [DESCRIPCION_CSMO] [VARCHAR ](50), 
    [NUM_RUE] INTEGER, 
    [CTE] FLOAT, 
    [LECT_anterior] VARCHAR(9), 
    [fecha_lect_anterior] VARCHAR(8), 
    [CSMO_anterior] VARCHAR(9), 
    [NIS_RAD] [VARCHAR ](7) NOT NULL ON CONFLICT IGNORE, 
    [Lect_min] [NUMERIC ](10), 
    [Lect_max] [NUMERIC ](10), 
    [Marca_medidor] varchar(100), 
    [Constante] INT DEFAULT 1, 
    CONSTRAINT [APACONENUNIQUE] UNIQUE([NUM_OS], [CO_MARCA], [NUM_APA], [TIP_CSMO], [NIS_RAD]) ON CONFLICT REPLACE);
    
    CREATE INDEX [APACONEN_INUM_APA] ON [APACONEN] ([NUM_APA] ASC);
    
    CREATE INDEX [APACONEN_INUM_OS] ON [APACONEN] ([NUM_OS] ASC);
    
    
    
    
    CREATE TABLE [APARATOS] (
    [NUM_OS] VARCHAR(8) NOT NULL ON CONFLICT IGNORE, 
    [NIS_RAD] VARCHAR(7) NOT NULL ON CONFLICT IGNORE, 
    [NUM_APA] VARCHAR(20) NOT NULL ON CONFLICT IGNORE, 
    [CO_MARCA] VARCHAR(5), 
    [TIP_APA] VARCHAR(5), 
    [EST_APA] VARCHAR(5), 
    [AOL_APA] VARCHAR(4), 
    [TIP_INTENSIDAD] VARCHAR(5), 
    [TIP_FASE] VARCHAR(5), 
    [TIP_TENSION] VARCHAR(5), 
    [F_INST] VARCHAR(8), 
    [F_FABRIC] VARCHAR(8), 
    [CSMO_PROM] VARCHAR(9),
    [MC_CODE] VARCHAR(5),
    [COM_TYPE] numeric(1) default 2,
    [CTE_APA] FLOAT,
    CONSTRAINT [APARATOSUNIQUE] UNIQUE([NUM_OS], [NIS_RAD], [NUM_APA]) ON CONFLICT  IGNORE);
    
    CREATE INDEX [APARATOS_INUM_OS] ON [APARATOS] ([NUM_OS] ASC);
    
    CREATE INDEX [INUM_APA] ON [APARATOS] ([NUM_APA] ASC);
    
    
    CREATE TABLE [APARATOS_CSMO_NUE] (
    [NUM_OS] VARCHAR(8), 
    [NIS_RAD] VARCHAR(7),
    [NUM_APA] VARCHAR(20),
    [CO_MARCA] VARCHAR(5),
    [TIP_CSMO] VARCHAR(5),
    [NUM_RUE] INT,
    [COEF_PER] numeric(18,5),
    [CTE] numeric(18,7),
    [LECTURA] VARCHAR(10));
    
    
    CREATE TABLE [APARATOS_ENV] (
    [NUM_OS] VARCHAR(8),
    [NIS_RAD] VARCHAR(7), 
    [NUM_APA] VARCHAR(20), 
    [CO_MARCA] VARCHAR(5), 
    [TIP_CSMO] VARCHAR(5),
    [TIP_APARATO] VARCHAR(5),
    [NUM_RUE] INTEGER,
    [COEF_PER] FLOAT,
    [CTE] FLOAT,
    [LECTURA] VARCHAR(8));
    
    
    
    CREATE TABLE RUTAS ( 
    ID NUMBER(11) NOT NULL, 
    CICLO VARCHAR2(5) NULL, 
    RUTA VARCHAR2(5) NULL, 
    ITINERARIO VARCHAR2(5) NULL, 
    PLAN VARCHAR2(5) NULL,
    ANIO VARCHAR2(10) NULL,
    CANT_total NUMBER(11) NOT NULL,  
    Cant_leida NUMBER(11) NOT NULL default 0,  
    FECHA_GENERACION  VARCHAR2(10)   NULL,
    FECHA_ESTIMADA_RESOLUCION  VARCHAR2(10)NULL,
    OFICINA  VARCHAR2(5) NOT NULL default '' );
    
    
    CREATE TABLE ObservacionesXanomalia ( 
    anomalia  VARCHAR2(10)   NULL,
    observacion  VARCHAR2(10) NULL,
    CONSTRAINT [] PRIMARY KEY ([anomalia], [observacion]) ON CONFLICT IGNORE);
    
    CREATE TABLE [APARATOS_MODIF] (
    [NUM_OS] VARCHAR(8), 
    [NIS_RAD] VARCHAR(7),
    [NUM_APA] VARCHAR(20),
    [CO_MARCA] VARCHAR(5),
    [TIP_APA] VARCHAR(5),
    [CO_PROP_APA] VARCHAR(5), 
    [TIP_FASE] VARCHAR(5), 
    [TIP_TENSION] VARCHAR(5),
    [TIP_INTENSIDAD] VARCHAR(5),
    [MC_CODE] VARCHAR(5),
    [COM_TYPE] numeric(1) default 2,
    [CTE_APA] FLOAT,
    [REGULADOR] VARCHAR(5),
    [TIP_MATERIAL] VARCHAR(5),
    [TIP_NATUR] VARCHAR(5));
    
    
    CREATE TABLE [APARATOS_NUE] (
    [NUM_OS] VARCHAR(8),
    [NIS_RAD] VARCHAR(7),
    [NUM_APA] VARCHAR(20),
    [CO_MARCA] VARCHAR(5),
    [TIP_APA] VARCHAR(5),
    [CO_PROP_APA] VARCHAR(5), 
    [AOL_APA] INTEGER, 
    [TIP_FASE] VARCHAR(5), 
    [TIP_TENSION] VARCHAR(5), 
    [F_INST] VARCHAR(19), 
    [TIP_INTENSIDAD] VARCHAR(5),
    [MC_CODE] VARCHAR(5),
    [COM_TYPE] numeric(1) default 2, 
    [CTE_APA] numeric(18,5), 
    [F_FABRIC] VARCHAR(19), 
    [F_UREVIS] VARCHAR(19), 
    [REGULADOR] VARCHAR(5), 
    [DIMEN_CONEX] numeric(18,5), 
    [F_PROX_CALIBRACION] VARCHAR(19), 
    [F_PROX_VERIFICACION] VARCHAR(19), 
    [TIP_MATERIAL] VARCHAR(5), 
    [TIP_NATUR] VARCHAR(5),
    [DIAMETRO] numeric(18,5),
    [ALTA] VARCHAR(1));
    
    
    CREATE TABLE CODIGOS (COD VARCHAR (5), DESC_COD VARCHAR (80), TIPO_ORDEN STRING (10));
    
    CREATE INDEX ICOD ON CODIGOS (COD ASC);
    
    CREATE TABLE anomalias (codigo varchar(10) not null ON CONFLICT Replace, codigo_corto VARCHAR(5),  descripcion VARCHAR(100), prioridad int, tipo_anom_lect VARCHAR(5), constraint [anomalia_pk] PRIMARY KEY (codigo) ON CONFLICT REPLACE); 
    CREATE INDEX [idx_anom_lect] ON [anomalias] ([tipo_anom_lect]); 
    
    CREATE TABLE [CONFIGURACION] (
    [PARAMETRO] varchar(100),[VALOR]varchar(500),
    CONSTRAINT [CONFIG_PK] PRIMARY KEY ([PARAMETRO]) ON CONFLICT REPLACE);
    
    CREATE TABLE [CONSUAPA] ([TIP_CSMO] VARCHAR(5) NOT NULL ON CONFLICT ROLLBACK,[TIP_APA] VARCHAR(5) NOT NULL ON  CONFLICT ROLLBACK,[IND_BAJA_TEN] VARCHAR(2),CONSTRAINT [CONSUAPAUNIQUE] UNIQUE([TIP_CSMO], [TIP_APA]) ON CONFLICT IGNORE);
    
    CREATE INDEX [ITIP_APA] ON [CONSUAPA] ([TIP_APA] ASC);
    
    CREATE INDEX [ITIP_CSMO_OS] ON [CONSUAPA] ([TIP_CSMO] ASC);
    
    
    CREATE TABLE [DATOSUM] (
    [NUM_OS] [NVARCHAR ] NOT NULL ON CONFLICT REPLACE CONSTRAINT [unqDATOSSUM] UNIQUE ON CONFLICT REPLACE, 
    [NIS_RAD] [VARCHAR ] NOT NULL ON CONFLICT REPLACE, 
    [SEC_NIS] [VARCHAR ] NOT NULL ON CONFLICT IGNORE, 
    [NIC] [VARCHAR ] NOT NULL ON CONFLICT IGNORE, 
    [NIF] VARCHAR(10), 
    [TIP_SERV] [VARCHAR ], 
    [TIP_SUMINISTRO] [VARCHAR ], 
    [COD_TAR] [VARCHAR ], 
    [TIP_CONEXION] [VARCHAR ], 
    [TIP_TENSION] [VARCHAR ], 
    [POT] [VARCHAR ], 
    [NUM_EXP] [VARCHAR ], 
    [NUM_RE] [VARCHAR ], 
    [RUTA] [VARCHAR ], 
    [RUTAITIN] varchar(10), 
    [NUM_ITIN] [VARCHAR ], 
    [MUNICIPIO] [VARCHAR ], 
    [LOCALIDAD] [VARCHAR ], 
    [DEPARTAMENTO] [VARCHAR ], 
    [TIP_VIA] [VARCHAR ], 
    [CALLE] [VARCHAR ], 
    [NUM_PUERTA] [VARCHAR ], 
    [DUPLICADOR] [VARCHAR ], 
    [CGV_SUM] [VARCHAR ], 
    [NOM_FINCA] [VARCHAR ], 
    [REF_DIR] [VARCHAR ], 
    [ACC_FINCA] [VARCHAR ], 
    [acceso_suministro] VARCHAR(255), 
    [APART_POSTAL] [VARCHAR ], 
    [APE1_CLI] [VARCHAR ], 
    [APE2_CLI] [VARCHAR ], 
    [NOM_CLI] [VARCHAR ], 
    [TFNO_CLI] [VARCHAR ], 
    [TIP_CLI] [VARCHAR ], 
    [DIRECCION] [VARCHAR ], 
    [TIP_CONEXION_SGD] [VARCHAR ], 
    [MATRICULA_SGD] [VARCHAR ], 
    [MATRICULA_CT] [VARCHAR ], 
    [TIP_PROP_TR] [VARCHAR ], 
    [DIRECCION_BDI] [VARCHAR ], 
    [LOCALIDAD_BDI] [VARCHAR ], 
    [Estado_serv] [REAL ], 
    [ref_direccion] varchar(255), 
    [acceso_direccion] VARCHAR(255), 
    CONSTRAINT [sqlite_autoindex_DATOSUM_1] PRIMARY KEY ([NUM_OS]) ON CONFLICT REPLACE);
    
    CREATE INDEX [INIC] ON [DATOSUM] ([NIC] ASC);
    
    CREATE INDEX [INIS_RAD] ON [DATOSUM] ([NIS_RAD] ASC);
    
    CREATE INDEX [ISEC_NIS] ON [DATOSUM] ([SEC_NIS] ASC);
    
    
    
    
    
    
    CREATE TABLE `desc_anomalias` (
    `num_os` varchar(20) NOT NULL,
    `id_anomalia` varchar(5) NOT NULL,
    `fecha_hora_registro` varchar(20) NOT NULL,
    `id_paso_accion` varchar(5)  NULL,`id_observacion` varchar(10) NULL,
    `comentario` varchar(250) NULL,
    CONSTRAINT ORDENESUNIQUE UNIQUE (
    NUM_OS,
    ID_ANOMALIA,
    FECHA_HORA_REGISTRO
    )
    ON CONFLICT IGNORE 
    
    );
    
    
    CREATE TABLE `desc_aparatos_alta` (
    `num_os` varchar(20) NOT NULL,
    `secuencia_registro` smallint(6) NOT NULL,
    `id_marca` varchar(5) NOT NULL,
    `numero_medidor` varchar(20) NOT NULL,
    `num_ruedas` tinyint(2) DEFAULT NULL,
    `id_tipo_servicio` char(1) DEFAULT NULL,
    `constante` varchar(1) DEFAULT '0',  
    lectura int,  
    fecha_hora_lectura varchar(20), 
    [num_serie_anterior] varchar2(50),   
    [num_serie_posterior] VARCHAR2(50), 
    [nif_anterior] varchAR2(50), 
    [nif_posterior] varchar2(50), 
    [observacion] vaRCHAR2(250)  
    
    );
    
    
    CREATE TABLE `desc_aparatos_modif` (
    `num_os` varchar(20) NOT NULL,
    `secuencia_registro` smallint(6) NOT NULL,
    `id_marca` varchar(5) DEFAULT NULL,
    `numero_medidor` varchar(20) DEFAULT NULL, 
    [observacion] vARCHAR(250),
    [lectura] INT DEFAULT 0
    );
    
    
    CREATE TABLE `desc_datos_cliente` (
    `num_os` varchar(20) NOT NULL,
    `secuencial_registro` int(6) NOT NULL,
    `nombre_cliente` varchar(100) DEFAULT NULL,
    `telefono_cliente` varchar(30) DEFAULT NULL,
    `email_cliente` varchar(150) DEFAULT NULL,
    `marca_medidor` varchar(150) DEFAULT NULL,
    `numero_medidor` varchar(20) DEFAULT NULL,
    `comentario` varchar(255) DEFAULT NULL
    );
    
    
    CREATE TABLE desc_fotos (
    num_os varchar (20) NOT NULL, 
    fecha_hora_registro varchar (20) NOT NULL, 
    fecha_foto varchar (8), 
    hora_foto varchar (6), 
    id_unidad_negocio varchar (5) DEFAULT NULL, 
    nis varchar (10) DEFAULT NULL, 
    descripcion_foto varchar (100) DEFAULT NULL, 
    id_paso_accion varchar (5) DEFAULT NULL, 
    foto CLOB, 
    enviada int default 0, 
    path_foto varchar(255),
    PRIMARY KEY (num_os, fecha_hora_registro), 
    CONSTRAINT desc_fotos_UNIQUE UNIQUE (NUM_OS, fecha_hora_registro) ON CONFLICT IGNORE);
    
    
    CREATE TABLE desc_indicadores (
    num_os VARCHAR (20) NOT NULL, 
    fecha_hora_registro VARCHAR (20) NOT NULL,  
    id_accion_paso VARCHAR (5) DEFAULT NULL, 
    indicador VARCHAR (50) DEFAULT NULL, 
    valor_indicador VARCHAR (50) DEFAULT  NULL, 
    PRIMARY KEY (num_os, fecha_hora_registro), 
    CONSTRAINT desc_idicadores_UNIQUE UNIQUE (num_os,  fecha_hora_registro) ON CONFLICT IGNORE);
    
    
    CREATE TABLE desc_lecturas (
    num_os             VARCHAR (20)  NOT NULL,
    secuencia_registro SMALLINT (6)  DEFAULT NULL,
    id_marca           VARCHAR (5)   NOT NULL,
    numero_medidor     VARCHAR (20)  NOT NULL,
    id_tipo_consumo    VARCHAR (5)   NOT NULL,
    id_tipo_aparato    VARCHAR (5)   DEFAULT NULL,
    coef_perdida       VARCHAR (20)  DEFAULT NULL,
    constante          TINYINT (4)   DEFAULT '1',
    cantidad_intentos int default 0,
    resultado int default 0,consumo int default 0,
    consulto_historico int default 0,
    lectura            MEDIUMINT (9) DEFAULT NULL, 
    lecturas_ingresadas varchar(250) default null,
    id_paso_accion     VARCHAR (5)   NOT NULL,
    PRIMARY KEY (
    num_os,
    id_marca,
    numero_medidor,
    id_tipo_consumo
    ),
    CONSTRAINT desc_lecturas_UNIQUE UNIQUE (
    NUM_OS,
    id_marca,
    numero_medidor,
    id_tipo_consumo
    )
    ON CONFLICT IGNORE
    );
    
    
    CREATE TABLE `desc_materiales` (
    `num_os` varchar(20) NOT NULL,
    `id_grupo_material` varchar(20) NOT NULL,
    `id_material` varchar(20) NOT NULL,
    `cantidad` decimal(5,2) DEFAULT NULL,
    `id_paso_accion` varchar(5) DEFAULT NULL,
    PRIMARY KEY (`num_os`,`id_grupo_material`,`id_material`)
    CONSTRAINT desc_materiales_UNIQUE UNIQUE (
    `num_os`,`id_grupo_material`,`id_material`
    )
    ON CONFLICT IGNORE 
      
    );
    
    
    CREATE TABLE `desc_observaciones` (
    `num_os` varchar(20) NOT NULL,
    `fecha_hora_registro` varchar(20) NOT NULL,
    `observacion` varchar(255) DEFAULT NULL,
    `id_paso_accion` varchar(5) DEFAULT NULL ,
    PRIMARY KEY (`num_os`,`fecha_hora_registro`)
    CONSTRAINT desc_observaciones_UNIQUE UNIQUE (
    `num_os`,`fecha_hora_registro`
    )
    ON CONFLICT IGNORE 
      
    );
    
    
    CREATE TABLE desc_ordenes (num_os varchar (20) NOT NULL, id_problema varchar (5) DEFAULT NULL, estado_os varchar (5)  NOT NULL, nis varchar (10) NOT NULL, nic varchar (10) NOT NULL, secuencial_registro smallint (6) NOT NULL,  fecha_resolucion varchar (8), fecha_hora_inicio_orden varchar (20) NOT NULL, fecha_hora_fin_orden varchar (20) NOT  NULL, fecha_hora_descarga varchar (20), id_tecnico varchar (20) NOT NULL,observacion_problema varchar(255), latitud  varchar (20) DEFAULT NULL, longitud varchar (20) DEFAULT NULL, ind_sospechosa char (1) DEFAULT '0', secuencia_real  INTEGER, id_reduccion STRING DEFAULT TQ000, offline integer default 0, [ruta] VARCHAR2(20),  PRIMARY KEY (num_os), CONSTRAINT  desc_ordenes_UNIQUE UNIQUE (num_os) ON CONFLICT IGNORE);
    
    
    CREATE TABLE `desc_visita` (
    `num_os` varchar(20) NOT NULL,
    `fh_visita` varchar(20) DEFAULT NULL,
    `id_accion_ejecutada` varchar(5) NOT NULL DEFAULT 'VA001',
    `observacion` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`num_os`,`id_accion_ejecutada`)
    CONSTRAINT desc_visita_UNIQUE UNIQUE (
    `num_os`,`id_accion_ejecutada`
    )
    ON CONFLICT IGNORE 
      
    );
    
    
    CREATE TABLE ESTADOS (ESTADO VARCHAR(5), DESC_EST VARCHAR(80));
    
    CREATE INDEX IESTADO ON ESTADOS (ESTADO ASC);
    
    
    CREATE TABLE [ORDENES] (
    [NUM_OS] [VARCHAR ](8) NOT NULL ON CONFLICT IGNORE, 
    [TIP_OS] [VARCHAR ](5),
    [TIP_SERV] [VARCHAR ](5), 
    [F_GEN] [VARCHAR ](8), 
    [F_ESTM_REST] [VARCHAR ](8), 
    [HORA_CITA] [VARCHAR ](5), 
    [CO_PRIOR_ORD] [VARCHAR ](5), 
    [NIS_RAD] [VARCHAR ](7) NOT NULL ON CONFLICT IGNORE, 
    [NIC] [VARCHAR ](7) NOT NULL ON CONFLICT IGNORE, 
    [SEC_NIS] [VARCHAR ](2) NOT NULL ON CONFLICT IGNORE, 
    [NUM_LOTE] [VARCHAR ](12), 
    [COD_EMP_ASIG] [VARCHAR ](6), 
    [NUM_CAMP] [VARCHAR ](5), 
    [IND_MAT_UUCC] [VARCHAR ](1), 
    [IND_ACTA] [VARCHAR ](1), 
    [COMENT_OS] [VARCHAR ](250), 
    [COMENT_OS2] [VARCHAR ](100), 
    [DESC_TIPO_ORDEN] [VARCHAR ](80), 
    [DESC_COD_PRIORIDAD] [VARCHAR ](80), 
    [DIRECCION] [VARCHAR ](45), 
    [RUTAITIN] [VARCHAR ](20), 
    [ESTADO] [VARCHAR ](1), 
    [ENVIADO] [VARCHAR ](1) DEFAULT '0', 
    [ORD_DISPONIBLE] [VARCHAR ](2) DEFAULT '99', 
    [SECUENCIA] INTEGER DEFAULT 0, 
    [ciclo] VARCHAR(10), 
    [ruta] VARCHAR(10), 
    [itinerario] VARCHAR(10), 
    [acceso_suministro] VARCHAR(255), [ref_direccion] varchar(255), 
    CONSTRAINT [ORDENESUNIQUE] UNIQUE([NUM_OS], [NIS_RAD], [NIC], [SEC_NIS]) ON CONFLICT IGNORE);
    
    CREATE INDEX [IORDENES] ON [ORDENES] ([NUM_OS] ASC);
    
    CREATE TABLE TIEMPOS (  
    FECHAHORA TEXT (14), 
    ACTIVIDAD VARCHAR (20),
    DATO VARCHAR (200),
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    REF_ID INTEGER,
    ID_TECNICO VARCHAR (20),
    LATITUD TEXT (20),
    LONGITUD VARCHAR (20),
    enviado INTEGER (1) DEFAULT (0)
    );
    
    CREATE TABLE [CONFIGINCIDENCIAS] 
    (id_tipo_orden VARCHAR (5) NOT NULL, id_tipo VARCHAR (5) NOT NULL, codigo VARCHAR (5) NOT NULL, descripcion VARCHAR  (30) NOT NULL, foto_obligatoria CHAR (1) DEFAULT '0', observacion_obligatoria CHAR (1) DEFAULT '0', datos_medidor  CHAR (1) DEFAULT '0', observacion_tabulada char(1) default '0', PRIMARY KEY (id_tipo_orden, id_tipo, codigo));
    
    CREATE TABLE [RESULORD] (
    [NUM_OS] VARCHAR(8),
    [NIS_RAD] VARCHAR(7),
    [NIC] VARCHAR(7),
    [SEC_NIC] VARCHAR(2),
    [NUM_LOTE] VARCHAR(12),
    [F_RESUL] VARCHAR(19),
    [TRANSFORMADOR] VARCHAR(10),
    [EST_OS] VARCHAR(5),
    [IND_MAT_UUCC] VARCHAR(1),
    [COD_EJECUTOR] INTEGER,
    [COD_AUXILIAR] INTEGER,
    [NUM_ACTA] VARCHAR(20), 
    [LATITUD]numeric(14,7), 
    [LONGITUD]numeric(14,7) );
    
    
    CREATE TABLE TARIFAS (COD_TAR VARCHAR(3), DESC_TAR VARCHAR(30));
    
    CREATE INDEX ICOD_TAR ON TARIFAS (COD_TAR ASC);
    
    
    CREATE TABLE TIPOS (TIPO VARCHAR(5), DESC_TIPO VARCHAR(80));
    
    CREATE INDEX ITIPO ON TIPOS (TIPO ASC);
     
     
    CREATE TABLE [USUARIO] (
    [NOMBRE_USUARIO] VARCHAR(30), 
    [PASSWORD] VARCHAR(8), 
    [ACTUALIZAR_PASSWORD] VARCHAR(1), 
    [ENVIAR_NUEVO_PASSWORD] VARCHAR(1));


    """
    	
    return _sSchemma