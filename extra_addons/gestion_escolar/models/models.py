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

    persona_id = fields.Many2one('res.partner', string='Persona', required=True)
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    gestion_id = fields.Many2one('gestion_escolar.gestion', string='Gestion', required=True)
    fecha_inscripcion = fields.Date(string='Fecha de Inscripción', required=True)
    lead_id = fields.Many2one('crm.lead', string='Lead CRM')   

class gestion(models.Model): 
    _name = 'gestion_escolar.gestion' 
    _description = 'Gestion Escolar' 
 
    name = fields.Char(string='Nombre', required=True) 
    fecha_inicio = fields.Date(string='Fecha Inicio') 
    fecha_final = fields.Date(string='Fecha Final') 

class padre(models.Model):
    _name = 'gestion_escolar.padre'
    _description = 'Padre o Madre del Estudiante'

    name = fields.Char(string='Nombre', required=True)
    padre_id = fields.Many2one('res.partner', string='Padre', required=True)
    alumno_ids = fields.Many2many('res.partner', string='Alumnos', domain=[('customer_rank', '>', 0)])
    
class profesor(models.Model):
    _name = 'gestion_escolar.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre', required=True)
    materia_ids = fields.One2many('gestion_escolar.materia', 'profesor_id', string='Materias')  
    
class pago_mensualidad(models.Model):
    _name = 'gestion_escolar.pago_mensualidad'
    _description = 'Pago de Mensualidad'

    alumno_id = fields.Many2one('res.partner', string='Alumno', required=True)
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
    _description = 'Asistencia del Alumno'

    fecha = fields.Date(string='Fecha', required=True)
    alumno_id = fields.Many2one('res.partner', string='Alumno', required=True)
    profesor_id = fields.Many2one('gestion_escolar.profesor', string='Profesor', required=True)

class horario(models.Model):
    _name = 'gestion_escolar.horario'
    _description = 'Horario'

    name = fields.Char(string='Nombre', required=True)
    hora_inicio = fields.Float(string='Hora de Inicio', required=True)
    hora_fin = fields.Float(string='Hora de Fin', required=True)

class curso(models.Model):
    _name = 'gestion_escolar.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre', required=True)
    nivel = fields.Selection([('primaria', 'Primaria'), ('secundaria', 'Secundaria')], string='Nivel', required=True)
    grado = fields.Char(string='Grado', required=True)
    turno = fields.Selection([('mañana', 'Mañana'), ('tarde', 'Tarde')], string='Turno', required=True)
    paralelo_id = fields.Many2one('gestion_escolar.paralelo', string='Paralelo', required=True)

class paralelo(models.Model): 
    _name = 'gestion_escolar.paralelo' 
    _description = 'Paralelo' 
 
    descripcion = fields.Text(string='Descripción') 
    
class materia(models.Model):
    _name = 'gestion_escolar.materia'
    _description = 'Materia'

    name = fields.Char(string='Nombre', required=True)
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    aula_id = fields.Many2one('gestion_escolar.aula', string='Aula', required=True)
    horario_id = fields.Many2one('gestion_escolar.horario', string='Horario', required=True)
    profesor_id = fields.Many2one('gestion_escolar.profesor', string='Profesor', required=True)
    boletin_id = fields.Many2one('gestion_escolar.boletin_alumno', string='Boletín de Alumno')
    
#Notas y Calificaciones   
class planificacion_examen(models.Model):
    _name = 'gestion_escolar.planificacion_examen'
    _description = 'Planificacion de los examenes'

    materia_id = fields.Many2one('gestion_escolar.materia', string='Materia', required=True)
    profesor_id = fields.Many2one('gestion_escolar.profesor', string='Profesor', required=True)
    fecha = fields.Date(string='Fecha', required=True) 
    
class nota_alumno(models.Model):
    _name = 'gestion_escolar.nota_alumno'
    _description = 'Nota de Alumno'

    alumno_id = fields.Many2one('res.partner', string='Alumno', required=True)
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    materia_id = fields.Many2one('gestion_escolar.materia', string='Materia', required=True)
    profesor_id = fields.Many2one('gestion_escolar.profesor', string='Profesor', required=True)
    planificacion_examen_id = fields.Many2one('gestion_escolar.planificacion_examen', string='Planificacion Examen', required=True)
    ponderacion = fields.Float(string='Ponderación', required=True)
    boletin_id = fields.Many2one('gestion_escolar.boletin_alumno', string='Boletín de Alumno') 
    
class boletin_alumno(models.Model):
    _name = 'gestion_escolar.boletin_alumno'
    _description = 'Boletín de Alumno'

    alumno_id = fields.Many2one('res.partner', string='Alumno', required=True)
    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    gestion_id = fields.Many2one('gestion_escolar.gestion', string='Gestion', required=True)
    profesor_id = fields.Many2one('gestion_escolar.profesor', string='Profesor', required=True)
    materia_ids = fields.One2many('gestion_escolar.materia', 'boletin_id', string='Materias')
    nota_ids = fields.One2many('gestion_escolar.nota_alumno', 'boletin_id', string='Notas')
    
#Informacion
class reporte(models.Model):
    _name = 'gestion_escolar.reporte'
    _description = 'Reporte'

    curso_id = fields.Many2one('gestion_escolar.curso', string='Curso', required=True)
    deudores_ids = fields.Many2many('res.partner', string='Deudores') 
    
class Anuncio(models.Model):
    _name = 'gestion_escolar.anuncio'
    _description = 'Anuncio'

    titulo = fields.Char(string='Título', required=True)
    descripcion = fields.Text(string='Descripción', required=True)

  