from django.db import migrations


PROCEDURES = [
    {
        'name': 'Aplazamiento de uso de derecho de matrícula para admitidos de posgrado',
        'official_description': 'Solicitud de postergación del inicio de estudios dirigida a aspirantes admitidos en especializaciones, maestrías o doctorados que no pueden cursar su primer periodo académico por causas debidamente justificadas y soportadas. Permite conservar la calidad de admitido por un periodo académico adicional.',
        'type': 'posgrado',
        'department': 'Oficina de Asuntos Estudiantiles / Consejo de Facultad',
    },
    {
        'name': 'Apoyo alimentario',
        'official_description': 'Subsidio de alimentación en especie consistente en servicios diarios de desayuno, almuerzo o cena dirigidos a estudiantes en condiciones demostradas de vulnerabilidad socioeconómica. Exige la valoración mediante el Instrumento para la Valoración Socioeconómica y el cumplimiento de 16 a 20 horas de corresponsabilidad semestral en dependencias de la universidad.',
        'type': 'bienestar',
        'department': 'División de Gestión y Fomento Socioeconómico (Dirección de Bienestar Universitario)',
    },
    {
        'name': 'Autorización de carga inferior a la mínima',
        'official_description': 'Solicitud académica para inscribir menos de los diez créditos mínimos exigidos por el Estatuto Estudiantil durante un periodo semestral. Requiere una justificación documentada de tipo médico, laboral o socioeconómico, excepto cuando el estudiante requiera menos créditos para culminar su plan de estudios.',
        'type': 'pregrado',
        'department': 'Oficina de Asuntos Estudiantiles / Consejo de Facultad',
    },
    {
        'name': 'Cancelación de asignaturas',
        'official_description': 'Trámite para anular el registro de materias inscritas. Puede realizarse de forma libre a través del SIA hasta la semana ocho del semestre académico con pérdida de créditos, o bien de manera extemporánea justificada ante el Consejo de Facultad aportando certificados que acrediten fuerza mayor.',
        'type': 'academico',
        'department': 'Dirección del Área Curricular / Oficina de Asuntos Estudiantiles',
    },
    {
        'name': 'Cancelación de periodo académico',
        'official_description': 'Solicitud excepcional para anular la totalidad de asignaturas inscritas en un semestre en curso debido a fuerza mayor o caso fortuito. Su aprobación por el Consejo de Facultad restituye los créditos del estudiante, preserva su estatus activo y faculta la devolución proporcional de la matrícula de acuerdo con el avance del periodo.',
        'type': 'academico',
        'department': 'Consejo de Facultad / Secretaría de la Facultad',
    },
    {
        'name': 'Carnetización (Expedición de identificación institucional)',
        'official_description': 'Proceso de emisión física del documento oficial de identificación institucional para la comunidad universitaria. Requiere la solicitud de una cita digital, presentación presencial del documento de identidad civil, toma de fotografía y captura biométrica de huella digital.',
        'type': 'registro',
        'department': 'División de Registro y Matrícula',
    },
    {
        'name': 'Certificado de calificaciones (Certificado de notas)',
        'official_description': 'Expedición de constancias académicas detalladas con el promedio acumulado (PAPA), historial de materias cursadas y distinciones. Los estudiantes con matrícula activa pueden realizar la descarga inmediata de certificados estándar en formato digital PDF sin costo a través del portal SIA.',
        'type': 'registro',
        'department': 'División de Registro y Matrícula / Secretaría de la Facultad',
    },
    {
        'name': 'Descuento electoral',
        'official_description': 'Beneficio financiero que otorga un descuento del diez por ciento en el costo de los derechos de matrícula para estudiantes de pregrado o posgrado. Se solicita a través de los canales digitales de registro adjuntando el certificado de votación de los últimos comicios de orden nacional.',
        'type': 'registro',
        'department': 'División de Registro y Matrícula',
    },
    {
        'name': 'Devolución de dinero por concepto de matrícula y otros derechos',
        'official_description': 'Reembolso de montos económicos liquidados y pagados en exceso o no debidos, aplicable en casos de reservas de cupo aprobadas, reubicación socioeconómica, o retiros de cursos de educación continua informados antes del inicio del programa.',
        'type': 'financiero',
        'department': 'División de Registro y Matrícula / Sección de Presupuesto y Tesorería',
    },
    {
        'name': 'Doble titulación',
        'official_description': 'Solicitud académica que faculta a los estudiantes de pregrado para cursar un segundo programa curricular simultáneo dentro de la universidad tras completar su quinta matrícula y cumplir con los promedios y créditos exigidos por las facultades implicadas.',
        'type': 'academico',
        'department': 'Dirección del Área Curricular / Consejo de Facultad',
    },
    {
        'name': 'Examen de calificación de doctorado',
        'official_description': 'Evaluación académica obligatoria en el nivel de doctorado estructurada para evaluar el avance investigativo, la suficiencia conceptual y la viabilidad de la propuesta de tesis doctoral del estudiante ante un comité calificado.',
        'type': 'posgrado',
        'department': 'Oficina de Asuntos Estudiantiles / Comité de Programa de Posgrado',
    },
    {
        'name': 'Formalización de inscripción para admisión a pregrado',
        'official_description': 'Procedimiento obligatorio de registro para los aspirantes a programas curriculares de pregrado. Incluye el recaudo de los derechos de inscripción, diligenciamiento en línea de información socioeconómica e ingreso del número de registro del Examen de Estado Saber 11.',
        'type': 'admisiones',
        'department': 'Dirección Nacional de Admisiones',
    },
    {
        'name': 'Fraccionamiento de matrícula',
        'official_description': 'Trámite financiero que autoriza diferir el pago de los derechos de matrícula de pregrado en tres cuotas. El primer recibo cubre el treinta por ciento de la matrícula más sistematización, bienestar y seguro; las dos cuotas restantes equivalen cada una al treinta y cinco por ciento de la matrícula.',
        'type': 'financiero',
        'department': 'Dirección de Bienestar de la Facultad / Comité de Matrícula',
    },
    {
        'name': 'Homologación, convalidación y equivalencia de asignaturas',
        'official_description': 'Reconocimiento académico de créditos de asignaturas aprobadas con anterioridad en programas de la universidad o de otras instituciones. Requiere radicar la solicitud a través del SIA adjuntando los programas oficiales de las materias y el certificado de calificaciones original.',
        'type': 'academico',
        'department': 'Consejo de Facultad / Comité Asesor del Programa Curricular',
    },
    {
        'name': 'Inscripción a ceremonia de grado',
        'official_description': 'Postulación formal realizada en las fechas del calendario académico por estudiantes que han completado la totalidad de sus requisitos curriculares. Exige encontrarse a paz y salvo por todo concepto administrativo y de biblioteca.',
        'type': 'graduacion',
        'department': 'Secretaría de la Facultad / División de Registro y Matrícula',
    },
    {
        'name': 'Inscripción a prueba de certificación en inglés',
        'official_description': 'Trámite de registro obligatorio dirigido a estudiantes de pregrado para presentar el examen oficial de suficiencia lingüística que certifica el cumplimiento del requisito de idioma extranjero exigido por los programas curriculares.',
        'type': 'pregrado',
        'department': 'División de Registro y Matrícula',
    },
    {
        'name': 'Inscripción extemporánea de asignaturas',
        'official_description': 'Solicitud excepcional autorizada a estudiantes que no lograron registrar sus cursos en el periodo regular por razones de fuerza mayor técnica o personal debidamente documentadas.',
        'type': 'academico',
        'department': 'Oficina de Asuntos Estudiantiles / Áreas Curriculares',
    },
    {
        'name': 'Matrícula no oportuna',
        'official_description': 'Proceso de formalización del registro financiero de matrícula fuera de los plazos ordinarios de sede. Conlleva recargos económicos por concepto de extemporalidad y requiere que el estudiante no registre deudas previas con la universidad.',
        'type': 'academico',
        'department': 'Oficina de Asuntos Estudiantiles / Dirección de Área Curricular',
    },
    {
        'name': 'Modificación de datos del formulario de inscripción',
        'official_description': 'Trámite administrativo para corregir inconsistencias u omisiones en el correo electrónico o documento de identidad registrados en el formulario de inscripción de pregrado. Conlleva un costo pecuniario y la entrega formal del comprobante de pago con copia del documento oficial.',
        'type': 'admisiones',
        'department': 'Dirección Nacional de Admisiones',
    },
    {
        'name': 'Modificación de títulos, director o codirector de tesis de posgrado',
        'official_description': 'Registro formal de ajustes académicos relativos al título oficial del proyecto de investigación o al nombramiento de tutores, directores o codirectores académicos para el desarrollo del trabajo final de maestría o doctorado.',
        'type': 'posgrado',
        'department': 'Oficina de Asuntos Estudiantiles / Consejo de Facultad',
    },
    {
        'name': 'Movilidad académica entre sedes',
        'official_description': 'Proceso de intercambio que permite a estudiantes regulares cursar de uno a tres semestres académicos en una sede física de la universidad distinta a la de su ingreso original. El estudiante pierde definitivamente este beneficio si reprueba materias durante la estancia.',
        'type': 'movilidad',
        'department': 'Oficina de Relaciones Interinstitucionales (ORI) / Dirección Académica de Sede',
    },
    {
        'name': 'Paz y salvo de biblioteca',
        'official_description': 'Emisión de la solvencia institucional que valida que un usuario no tiene préstamos de material bibliográfico pendientes ni multas económicas en mora con el Sistema Nacional de Bibliotecas. Es indispensable para la renovación de matrícula y ceremonias de grado.',
        'type': 'biblioteca',
        'department': 'División de Bibliotecas / Sección de Servicios Bibliotecarios (SINAB)',
    },
    {
        'name': 'Planes de acondicionamiento físico',
        'official_description': 'Inscripción formal en programas estructurados de ejercicio y acondicionamiento deportivo dirigidos a la comunidad de docentes, estudiantes y personal administrativo, gestionados a través del portal SIBU.',
        'type': 'deportivo',
        'department': 'Sección o División de Actividad Física y Deporte (Dirección de Bienestar Universitario)',
    },
    {
        'name': 'Práctica Académica Especial (PAE)',
        'official_description': 'Formalización curricular de pasantías, prácticas profesionales y prácticas especiales de extensión desarrolladas por estudiantes de pregrado en empresas externas con convenios vigentes. Exige la formulación de planes de trabajo avalados por tutores académicos.',
        'type': 'practicas',
        'department': 'Dirección de Área Curricular / Oficina de Asuntos Estudiantiles',
    },
    {
        'name': 'Préstamo de implementos deportivos',
        'official_description': 'Préstamo temporal de material deportivo y lúdico para el aprovechamiento del tiempo libre de estudiantes, egresados y pensionados. Exige presentar el carné institucional vigente y encontrarse libre de sanciones en el área de bienestar.',
        'type': 'deportivo',
        'department': 'Sección o División de Actividad Física y Deporte (Dirección de Bienestar Universitario)',
    },
    {
        'name': 'Préstamo de material bibliográfico',
        'official_description': 'Servicio que autoriza retirar colecciones físicas de libros bajo modalidades de consulta interna, a domicilio, préstamos intersedes o convenios interbibliotecarios con entidades aliadas. La pérdida de libros exige reponer un ejemplar idéntico o equivalente.',
        'type': 'biblioteca',
        'department': 'División de Bibliotecas (SINAB)',
    },
    {
        'name': 'Recuperación de contraseña y cuenta institucional',
        'official_description': 'Gestión tecnológica para restablecer o modificar las credenciales del correo oficial y portal de servicios, tramitada en línea por el portal del sistema de cuentas o mediante radicación de solicitudes ante la mesa de soporte técnico.',
        'type': 'tecnologia',
        'department': 'Oficina de Tecnologías de la Información y las Comunicaciones (OTIC) / Dirección Nacional de Información Académica',
    },
    {
        'name': 'Refrendación de matrícula inicial para admitidos a pregrado',
        'official_description': 'Procedimiento de verificación de identidad y validación física de soportes académicos exigidos a los nuevos estudiantes admitidos para perfeccionar de forma legal y oportuna su matrícula inicial en la universidad.',
        'type': 'pregrado',
        'department': 'División de Registro y Matrícula',
    },
    {
        'name': 'Reingreso',
        'official_description': 'Solicitud de retorno académico dirigida a exestudiantes que perdieron su estatus regular. En pregrado exige un promedio acumulado (PAPA) mínimo de 2.7 y en posgrado un promedio igual o mayor a 3.5. El trámite no es viable si transcurren más de tres años consecutivos de desvinculación.',
        'type': 'academico',
        'department': 'Consejo de la Facultad / Comité Asesor del Programa Curricular',
    },
    {
        'name': 'Reserva de cupo adicional',
        'official_description': 'Solicitud de aplazamiento semestral para estudiantes que ya agotaron sus dos reservas automáticas de matrícula y presentan situaciones de fuerza mayor debidamente documentadas ante el Consejo de la Facultad con antelación.',
        'type': 'academico',
        'department': 'Oficina de Asuntos Estudiantiles / Consejo de Facultad',
    },
    {
        'name': 'Residencias universitarias (Gestión para el alojamiento)',
        'official_description': 'Adjudicación semestral de plazas en las casas universitarias u opciones de alojamiento operadas por bienestar universitario para estudiantes de pregrado con vulnerabilidad socioeconómica demostrada procedentes de otras regiones del país.',
        'type': 'vivienda',
        'department': 'Área de Gestión y Fomento Socioeconómico (Dirección de Bienestar Universitario)',
    },
    {
        'name': 'Semilleros de investigación (Registro y formalización)',
        'official_description': 'Inscripción formal en la plataforma oficial HERMES de grupos o semilleros de investigación, creación artística o extensión colectiva liderados por un docente tutor, validando la participación de estudiantes en actividades investigativas.',
        'type': 'investigacion',
        'department': 'Vicedecanatura de Investigación y Extensión / Dirección de Investigación de Sede',
    },
    {
        'name': 'Solicitud de cambio de nombre, apellido y/o sexo',
        'official_description': 'Actualización del registro académico oficial de la identidad civil de un estudiante con base en escrituras públicas notariales vigentes. Implica la reexpedición física del carné institucional con costo y el cambio del correo oficial institucional sin costo.',
        'type': 'registro',
        'department': 'División de Registro y Matrícula',
    },
    {
        'name': 'Traslado de programa curricular',
        'official_description': 'Proceso por el cual un estudiante matriculado cambia de programa de estudios dentro del mismo nivel. Si se radica antes de aprobar el treinta por ciento de los créditos, exige que el puntaje del examen de admisión original sea igual o superior al puntaje del último admitido regular en la carrera destino.',
        'type': 'academico',
        'department': 'Consejo de la Facultad Destino / Comité Asesor del Programa Curricular',
    },
]


def seed_procedures(apps, schema_editor):
    Procedure = apps.get_model('core', 'Procedure')
    for proc in PROCEDURES:
        Procedure.objects.get_or_create(
            name=proc['name'],
            defaults={
                'official_description': proc['official_description'],
                'type': proc['type'],
                'department': proc['department'],
            }
        )


def reverse_seed(apps, schema_editor):
    Procedure = apps.get_model('core', 'Procedure')
    names = [p['name'] for p in PROCEDURES]
    Procedure.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_add_vote_id'),
    ]

    operations = [
        migrations.RunPython(seed_procedures, reverse_seed),
    ]
