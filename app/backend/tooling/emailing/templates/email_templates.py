# import

# html new password confirm
def html_new_password_confirmation_temp(login_url: str) -> str:
    return f"""
                <table border="0" cellspacing="0" cellpadding="0" style="max-width:600px">
                    <tbody>
                        <tr height="16"></tr>
                        <tr>
                            <td>
                                <table bgcolor="#4184F3" width="100%" border="0" cellspacing="0" cellpadding="0"
                                    style="min-width:332px;max-width:600px;border:1px solid #e0e0e0;border-bottom:0;border-top-left-radius:3px;border-top-right-radius:3px">
                                    <tbody>
                                        <tr>
                                            <td height="72px" colspan="3"></td>
                                        </tr>
                                        <tr>
                                            <td width="32px"></td>
                                            <td
                                                style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:24px;color:#ffffff;line-height:1.25">
                                                Inicio de Sesión | Ingresar
                                            </td>
                                            <td width="32px"></td>
                                        </tr>
                                        <tr>
                                            <td height="18px" colspan="3"></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <table bgcolor="#FAFAFA" width="100%" border="0" cellspacing="0" cellpadding="0"
                                    style="min-width:332px;max-width:600px;border:1px solid #f0f0f0;border-bottom:1px solid #c0c0c0;border-top:0;border-bottom-left-radius:3px;border-bottom-right-radius:3px">
                                    <tbody>
                                        <tr height="16px">
                                            <td width="32px" rowspan="3"></td>
                                            <td></td>
                                            <td width="32px" rowspan="3"></td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <p>Estimado Usuario.</p>
                                                <p>Se registrado su contraseña nueva de acceso.</p>
                                                <p>
                                                   Por motivos de seguridad, le recomendamos mantener su contraseña de 
                                                   acceso de forma segura, evite escribirla en algún papel o superficie 
                                                   donde pueda quedar descubierta.
                                                </p>
                                                <p>
                                                    La seguridad del acceso al sistema es también responsabilidad suya.
                                                </p>
                                                <p>
                                                    Le invitamos a iniciar sesión en el siguiente link 
                                                    <a href="{login_url}"><b>Iniciar Sesión</b></a>
                                                </p>
                                                <p>Estamos para servirle!</p>
                                                <p>Ferretería Santa Lucía, Desamparados, Calle Fallas</p>
                                            </td>
                                        </tr>
                                        <tr height="32px"></tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>
            """


# html temp password sending
def html_temp_password_sending(temp: str) -> str:
    return f"""
            <table border="0" cellspacing="0" cellpadding="0" style="max-width:600px">
                <tbody>
                    <tr height="16"></tr>
                    <tr>
                        <td>
                            <table bgcolor="#4184F3" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #e0e0e0;border-bottom:0;border-top-left-radius:3px;border-top-right-radius:3px">
                                <tbody>
                                    <tr>
                                        <td height="72px" colspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td width="32px"></td>
                                        <td
                                            style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:24px;color:#ffffff;line-height:1.25">
                                            Contraseña Temporal
                                        </td>
                                        <td width="32px"></td>
                                    </tr>
                                    <tr>
                                        <td height="18px" colspan="3"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table bgcolor="#FAFAFA" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #f0f0f0;border-bottom:1px solid #c0c0c0;border-top:0;border-bottom-left-radius:3px;border-bottom-right-radius:3px">
                                <tbody>
                                    <tr height="16px">
                                        <td width="32px" rowspan="3"></td>
                                        <td></td>
                                        <td width="32px" rowspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <p>Estimado Usuario.</p>
                                            <p>Se ha generado una contraseña temporal para su acceso.</p>
                                            <div style="text-align:center">
                                                <p dir="ltr">
                                                    <strong style="text-align:center,font-size:25px;font-weight:bold">
                                                    {temp}
                                                    </strong>
                                                </p>
                                            </div>
                                            <p>
                                                Por motivos de seguridad, le recomendamos que inicie sesión lo antes 
                                                posible y cambie esta contraseña por una nueva de su elección.
                                            </p>
                                            <p>
                                                No comparta esta contraseña con nadie y evite almacenarla en lugares inseguros.
                                            </p>
                                            <p>Estamos para servirle!</p>
                                            <p>Ferretería Santa Lucía, Desamparados, Calle Fallas</p>
                                        </td>
                                    </tr>
                                    <tr height="32px"></tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        """


# html temp password with url sending
def html_temp_password_with_url_sending(temp: str, login_url: str) -> str:
    return f"""
            <table border="0" cellspacing="0" cellpadding="0" style="max-width:600px">
                <tbody>
                    <tr height="16"></tr>
                    <tr>
                        <td>
                            <table bgcolor="#4184F3" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #e0e0e0;border-bottom:0;border-top-left-radius:3px;border-top-right-radius:3px">
                                <tbody>
                                    <tr>
                                        <td height="72px" colspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td width="32px"></td>
                                        <td
                                            style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:24px;color:#ffffff;line-height:1.25">
                                            Contraseña Temporal
                                        </td>
                                        <td width="32px"></td>
                                    </tr>
                                    <tr>
                                        <td height="18px" colspan="3"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table bgcolor="#FAFAFA" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #f0f0f0;border-bottom:1px solid #c0c0c0;border-top:0;border-bottom-left-radius:3px;border-bottom-right-radius:3px">
                                <tbody>
                                    <tr height="16px">
                                        <td width="32px" rowspan="3"></td>
                                        <td></td>
                                        <td width="32px" rowspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <p>Estimado Usuario.</p>
                                            <p>Se ha generado una contraseña temporal para su acceso.</p>
                                            <div style="text-align:center">
                                                <p dir="ltr">
                                                    <strong style="text-align:center,font-size:25px;font-weight:bold">
                                                    {temp}
                                                    </strong>
                                                </p>
                                            </div>
                                            <p>
                                                Por motivos de seguridad, le recomendamos que inicie sesión lo antes 
                                                posible y cambie esta contraseña por una nueva de su elección.
                                            </p>
                                            <p>
                                                No comparta esta contraseña con nadie y evite almacenarla en lugares inseguros.
                                            </p>
                                            <p>
                                                Inicie sesión en el siguiente enlace para 
                                                realizar el cambio de contraseña: <a href="{login_url}"><b>Iniciar Sesión</b></a>
                                            </p>
                                            <p>Estamos para servirle!</p>
                                            <p>Ferretería Santa Lucía, Desamparados, Calle Fallas</p>
                                        </td>
                                    </tr>
                                    <tr height="32px"></tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        """


# html evaluation activate with url
def html_evaluation_activate_with_url_sending(type_of: str, login_url: str) -> str:
    return f"""
            <table border="0" cellspacing="0" cellpadding="0" style="max-width:600px">
                <tbody>
                    <tr height="16"></tr>
                    <tr>
                        <td>
                            <table bgcolor="#4184F3" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #e0e0e0;border-bottom:0;border-top-left-radius:3px;border-top-right-radius:3px">
                                <tbody>
                                    <tr>
                                        <td height="72px" colspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td width="32px"></td>
                                        <td
                                            style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:24px;color:#ffffff;line-height:1.25">
                                            Evaluación Activada | <b>{type_of.capitalize()}</b>
                                        </td>
                                        <td width="32px"></td>
                                    </tr>
                                    <tr>
                                        <td height="18px" colspan="3"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table bgcolor="#FAFAFA" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #f0f0f0;border-bottom:1px solid #c0c0c0;border-top:0;border-bottom-left-radius:3px;border-bottom-right-radius:3px">
                                <tbody>
                                    <tr height="16px">
                                        <td width="32px" rowspan="3"></td>
                                        <td></td>
                                        <td width="32px" rowspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <p>Estimado Usuario.</p>
                                            <p>Se encuentra activa la evaluación de {type_of.upper()}.</p>
                                            <p>
                                               La retroalimentación para los colaboradores es de suma importancia para 
                                               reconocimientos y áreas de mejora que se puedan atender. Considerar bien cada 
                                               respuesta y comentarios a requerir de la evaluación.
                                            </p>
                                            <p>
                                                Las respuestas contenidas en la evaluación son de carácter confidencial 
                                                y serán evaluadas y discutidas con su persona a cargo.
                                            </p>
                                            <p>
                                                Le invitamos a iniciar sesión en el siguiente link 
                                                <a href="{login_url}"><b>Iniciar Sesión</b></a>
                                            </p>
                                            <p>Estamos para servirle!</p>
                                            <p>Ferretería Santa Lucía, Desamparados, Calle Fallas</p>
                                        </td>
                                    </tr>
                                    <tr height="32px"></tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        """


# html evaluation results
def html_evaluation_results_sending(type_of: str, subject: object) -> str:
    return f"""
            <table border="0" cellspacing="0" cellpadding="0" style="max-width:600px">
                <tbody>
                    <tr height="16"></tr>
                    <tr>
                        <td>
                            <table bgcolor="#4184F3" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #e0e0e0;border-bottom:0;border-top-left-radius:3px;border-top-right-radius:3px">
                                <tbody>
                                    <tr>
                                        <td height="72px" colspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td width="32px"></td>
                                        <td
                                            style="font-family:Roboto-Regular,Helvetica,Arial,sans-serif;font-size:24px;color:#ffffff;line-height:1.25">
                                            Resultado de Evaluación | <b>{type_of.capitalize()}</b>
                                        </td>
                                        <td width="32px"></td>
                                    </tr>
                                    <tr>
                                        <td height="18px" colspan="3"></td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <table bgcolor="#FAFAFA" width="100%" border="0" cellspacing="0" cellpadding="0"
                                style="min-width:332px;max-width:600px;border:1px solid #f0f0f0;border-bottom:1px solid #c0c0c0;border-top:0;border-bottom-left-radius:3px;border-bottom-right-radius:3px">
                                <tbody>
                                    <tr height="16px">
                                        <td width="32px" rowspan="3"></td>
                                        <td></td>
                                        <td width="32px" rowspan="3"></td>
                                    </tr>
                                    <tr>
                                        <td>
                                            <p>Estimado(a) {subject._subj_name} {subject._subj_lastname} {subject._subj_lastname2}.</p>
                                            <p>Se encuentra a continuación los resultados de su evaluación {type_of.upper()}.</p>
                                            <p>
                                               Promedio de evaluación. <h3>{subject._avg}</h3>
                                            </p>
                                            <p>
                                               Encuentre su documento de evaluación adjunto para más detalles.
                                            </p>
                                            <p>
                                                Las respuestas contenidas en la evaluación son de carácter confidencial 
                                                y serán evaluadas y discutidas con su persona a cargo.
                                            </p>
                                            <p>Estamos para servirle!</p>
                                            <p>Ferretería Santa Lucía, Desamparados, Calle Fallas</p>
                                        </td>
                                    </tr>
                                    <tr height="32px"></tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        """
