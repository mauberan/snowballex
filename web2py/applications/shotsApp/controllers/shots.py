# -*- coding: utf-8 -*-
# try something like

import datetime

db = DAL('mysql://m30czfm31v0qd469:ltcgnxp4omt3hsa4@w1kr9ijlozl9l79i.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/etzwbbegjluy8glm')
currPath = URL(args=request.args, vars=request.get_vars, host=True)


def status():
    db.define_table('statuses', Field('name', type="string", unique="True"), Field('colorHex', type="string", unique='True'))
    db.statuses.validate_and_insert(name='Not Started', colorHex='#03eac1')
    db.statuses.validate_and_insert(name='WIP', colorHex='#ffb607')
    db.statuses.validate_and_insert(name='Need Fixing', colorHex='#ea03d4')
    db.statuses.validate_and_insert(name='Failed QA', colorHex='#ff2700')
    db.statuses.validate_and_insert(name='Rendered', colorHex='#E6E200')
    db.statuses.validate_and_insert(name='done', colorHex='#36d250')
    db.statuses.validate_and_insert(name='Deleted', colorHex='#0335ea')

    # statuses =  []
    # for row in db().select(db.statuses.ALL):
    #     statuses.append(row.name)

    db.define_table('shotsTable', Field('name', type="string",label='Name', required="True", unique="True", notnull="True"), Field(
        'modified', type="date", writeable="False", readable="True"), Field('framesNum', type="integer", label='Number of Frames'), Field('modifier', type="string", label='Modified By'), Field('status', notnull='True'), Field('active', type='boolean'), Field('description', type='text'))
    db.shotsTable.status.requires = IS_IN_DB(db, 'statuses.name',zero=None)

    # get all shots
    db.shotsTable.validate_and_insert(name='shot 08', modified='2019-4-4', framesNum=65, modifier='Ran', status='pis da', statusColor='kaki', active=True, description='who cates')
    db.shotsTable.id.readable = False


    shotlist = str(DIV(A('+ Create new Shot', _href=URL('status/'), _style='color: white'), _class='shot-list-item'))

    for row in db().select(db.shotsTable.ALL):
        shotStatus = db(db.statuses.name == row.status).select()


        # shotlist = shotlist + str(DIV(str(shotStatus)))
        shotlist = shotlist + str(DIV(A(row.name, _href=URL('status/' + str(row.id)), _style="color:" + shotStatus[0].colorHex + ";" ), _class='shot-list-item', _style="color:green;"))
        # shotlist = shotlist + u'<div class="shot-list-item"><a href="status/' + str(row.id) + u'>' + row.name + u'</a></div>'

    # deciding if its an update or insert form
    arg = request.args
    if len(arg) == 0:
        form = SQLFORM(db.shotsTable, formstyle='bootstrap4_inline')
    else:
       form = SQLFORM(db.shotsTable, int(arg[0]), formstyle='bootstrap4_inline')

    if request.post_vars:

        newColorHex = db(db.statuses.name == request.post_vars.status).select()

        if not request.post_vars.id:
        #     case where no id on post vars == new record inserted
        #  update the shots table after insertion
            db.shotsTable.validate_and_insert(name=request.post_vars.name, modified=datetime.date.today(),
                                          framesNum=request.post_vars.framesNum, modifier=request.post_vars.modifier,
                                          status=request.post_vars.status, statusColor=newColorHex[0].colorHex, active=request.post_vars.active,
                                          description=request.post_vars.description)
            redirect(currPath)

        else:
            # case where we got specific shot id to update
            updatingShot = db(db.shotsTable.id == request.post_vars.id).select().first()
            updatingShot.update_record(name=request.post_vars.name, modified=datetime.date.today(),
                                          framesNum=request.post_vars.framesNum, modifier=request.post_vars.modifier,
                                          status=request.post_vars.status, statusColor=newColorHex[0].colorHex, active=request.post_vars.active,
                                          description=request.post_vars.description)
            redirect(currPath)


    form['_style'] = ''
    for input in form.elements('input', _class='string'):
        input['_class'] = ''

    response.view = '../views/default/status.html'
    return dict(message=form, shotList=XML(shotlist))
