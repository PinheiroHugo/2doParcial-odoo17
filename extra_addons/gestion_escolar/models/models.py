# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _
import datetime
import logging

#Administracion y Admision
class inscripcion(models.Model):
    _name = 'gestion_escolar.inscripcion'
    _description = 'Inscripción'

    persona_id = fields.Many2one('res.partner', string='Alumno', required=True)
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    gestion_id = fields.Many2one('gestion_escolar.gestion', string='Gestion', required=True)
    fecha_inscripcion = fields.Date(string='Fecha de Inscripción', required=True)
    apoderado_id = fields.Many2one('gestion_escolar.apoderado', string='Apoderado', required=True)

class gestion(models.Model): 
    _name = 'gestion_escolar.gestion' 
    _description = 'Gestion Escolar' 
 
    name = fields.Char(string='Nombre', required=True) 
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True) 
    fecha_final = fields.Date(string='Fecha Final', required=True)
    cursos = fields.Many2many("gestion_escolar.curso")

class apoderado(models.Model):
    _name = 'gestion_escolar.apoderado'
    _description = 'Apoderado'

    name = fields.Many2one('res.partner', string='Apoderado', required=True)
    parentesco = fields.Text(string='Parentesco', required=True)
    mobile = fields.Char(related='name.mobile', string='Móvil', readonly=False)
    
class profesor(models.Model):
    _name = 'gestion_escolar.profesor'
    _description = 'Profesor'

    persona_id = fields.Many2one('hr.employee', string='Profesor', required=True)
    telefono = fields.Char(related='persona_id.work_phone', string='Teléfono', readonly=False)
    
class mensualidad(models.Model):
    _name = 'gestion_escolar.mensualidad'
    _description = 'Pago de Mensualidad'

    alumnos = fields.Many2many('gestion_escolar.inscripcion', string='Alumno')
    monto = fields.Float(string='Monto', required=True)
    mes = fields.Selection([
        ('enero', 'Enero'),
        ('febrero', 'Febrero'),
        ('marzo', 'Marzo'),
        ('abril', 'Abril'),
        ('mayo', 'Mayo'),
        ('junio', 'Junio'),
        ('julio', 'Julio'),
        ('agosto', 'Agosto'),
        ('septiembre', 'Septiembre'),
        ('octubre', 'Octubre'),
        ('noviembre', 'Noviembre'),
        ('diciembre', 'Diciembre'),
    ], string='Mes', required=True)
    nit = fields.Char(string='NIT', required=False)
    
#Clases y Horarios
class asistencia(models.Model):
    _name = 'gestion_escolar.asistencia'
    _description = 'Asistencia'

    fecha = fields.Date(string='Fecha', required=True)
    profesor = fields.Many2many('gestion_escolar.profesor', string='Profesor')
    alumnos = fields.Many2many('gestion_escolar.inscripcion', string='Alumno')
    

class horario(models.Model):
    _name = 'gestion_escolar.horario'
    _description = 'Horario'
    
    name = fields.Char(string='Nombre', required=True)
    dia = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ], string='Día', required=True)
    hora_inicio = fields.Float(string="Hora", help="Ingrese la hora en formato 24h")
    hora_fin = fields.Float(string="Hora", help="Ingrese la hora en formato 24h")
    materia_id = fields.Many2one("gestion_escolar.materia", string='Materia')

class curso(models.Model):
    _name = 'gestion_escolar.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre', required=True)
    nivel = fields.Selection([('primaria', 'Primaria'), ('secundaria', 'Secundaria')], string='Nivel', required=True)
    grado = fields.Char(string='Grado', required=True)
    turno = fields.Selection([('mañana', 'Mañana'), ('tarde', 'Tarde')], string='Turno', required=True)
    paralelo_id = fields.Many2one('gestion_escolar.paralelo', string='Paralelo')
    profesor = fields.Many2many('gestion_escolar.profesor', string='Profesor')
    horarios = fields.Many2many("gestion_escolar.horario")
    alumnos = fields.Many2many('gestion_escolar.inscripcion', string='Alumnos')

class paralelo(models.Model): 
    _name = 'gestion_escolar.paralelo' 
    _description = 'Paralelo' 
 
    name = fields.Char(string='Nombre del Paralelo', required=True)

class materia(models.Model):
    _name = 'gestion_escolar.materia'
    _description = 'Materia'

    name = fields.Char(string='Nombre', required=True)
    
#Notas y Calificaciones   
class plan_examen(models.Model):
    # _inherit = 'calendar.event'
    _name = 'gestion_escolar.plan_examen'
    _description = 'Plan de los examenes'

    fecha = fields.Datetime(string='Fecha', required=True)
    profesor = fields.Many2many('gestion_escolar.profesor', string='Profesor')
    materia_id = fields.Many2one('gestion_escolar.materia', string='Materia', required=True)
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    
class nota(models.Model):
    _name = 'gestion_escolar.nota'
    _description = 'Nota de Alumno'

    alumnos = fields.Many2many('gestion_escolar.inscripcion', string='Alumno')
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    materia_id = fields.Many2one('gestion_escolar.materia', string='Materia', required=True)
    profesor = fields.Many2many('gestion_escolar.profesor', string='Profesor', required=True)
    plan_examen_id = fields.Many2one('gestion_escolar.plan_examen', string='Plan Examen', required=True)
    ponderacion = fields.Float(string='Ponderación', required=True)
    boletin_id = fields.Many2one('gestion_escolar.boletin', string='Boletín de Alumno') 
    
class boletin(models.Model):
    _name = 'gestion_escolar.boletin'
    _description = 'Boletín de Alumno'

    alumnos = fields.Many2many('gestion_escolar.inscripcion', string='Alumno')
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    gestion_id = fields.Many2one('gestion_escolar.gestion', string='Gestion', required=True)
    profesor = fields.Many2many('gestion_escolar.profesor', string='Profesor', required=True)
    notas = fields.Many2many('gestion_escolar.nota', 'boletin_id', string='Notas')
    
#Informacion
class reporte(models.Model):
    _name = 'gestion_escolar.reporte'
    _description = 'Reporte'
    
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    mensualidades = fields.Many2many('gestion_escolar.mensualidad', string='Deudores')
    descripcion = fields.Selection([('si', 'Si'), ('no', 'No')], string='Debe', required=True)
    
class Anuncio(models.Model):
    _name = 'gestion_escolar.anuncio'
    _description = 'Anuncio'

    titulo = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción', required=True)

  